import streamlit as st
from pymongo import MongoClient
import pandas as pd
from collections import defaultdict

# --- This MUST be the first Streamlit command ---
st.set_page_config(layout="wide")

# --- Database Connection ---
@st.cache_resource
def init_connection():
    # Corrected MongoDB port
    return MongoClient('mongodb://localhost:27017/')

client = init_connection()

# --- Data Loading with Caching ---
@st.cache_data(ttl=600)
def get_data():
    db = client['medicine_reco']
    medicines = list(db.medicines.find())
    users = list(db.users.find())
    return medicines, users

medicines_data, users_data = get_data()

# --- SYMPTOM MAP ---
symptom_map = {
    "headache": "Analgesic", "fever": "Analgesic", "pain": "Analgesic", "body ache": "Analgesic",
    "allergy": "Antihistamine", "runny nose": "Antihistamine", "cold": "Antihistamine", "cough": "Antitussive",
    "acidity": "Antacid", "heartburn": "Antacid", "gas": "Antacid", "stomach ache": "Proton pump inhibitor", "indigestion": "Antacid",
    "infection": "Antibiotic", "sore throat": "Antibiotic"
}

# --- Recommendation Logic ---
def get_recommendations(user_id, search_query, medicines, users):
    scores = defaultdict(lambda: {'score': 0, 'reasons': []})
    
    user = next((u for u in users if u['_id'] == user_id), None)
    if not user:
        return pd.DataFrame()

    user_purchase_history_ids = {p['medicine_id'] for p in user.get('purchase_history', [])}

    match_score = 100
    purchase_history_score = 50
    collab_filter_score = 25

    if search_query:
        query = search_query.lower()
        matched_category = symptom_map.get(query)

        for med in medicines:
            med_id = med['_id']
            if matched_category and matched_category.lower() in med['category'].lower():
                scores[med_id]['score'] += match_score
                scores[med_id]['reasons'].append(f"Matches your search for '{query}'")
            elif query in med['name'].lower() or any(query in comp.lower() for comp in med['composition']):
                scores[med_id]['score'] += match_score
                scores[med_id]['reasons'].append(f"Name or composition matches '{query}'")

    for med_id in user_purchase_history_ids:
        if med_id in scores or not search_query: 
            scores[med_id]['score'] += purchase_history_score
            scores[med_id]['reasons'].append("Based on your frequent purchases.")

    similar_users = []
    for other_user in users:
        if other_user['_id'] != user_id:
            other_purchase_ids = {p['medicine_id'] for p in other_user.get('purchase_history', [])}
            if len(user_purchase_history_ids.intersection(other_purchase_ids)) >= 3:
                similar_users.append(other_purchase_ids)
    
    if similar_users:
        suggestions = defaultdict(int)
        for other_purchase_ids in similar_users:
            for med_id in other_purchase_ids:
                if med_id not in user_purchase_history_ids:
                    suggestions[med_id] += 1
        
        for med_id, count in suggestions.items():
            if count > 1:
                if med_id in scores or not search_query:
                    scores[med_id]['score'] += collab_filter_score
                    scores[med_id]['reasons'].append("Others with similar taste also bought this.")

    if not scores:
        return pd.DataFrame()

    reco_list = []
    for med_id, data in scores.items():
        med_info = next((m for m in medicines if m['_id'] == med_id), None)
        if med_info:
            reco_list.append({
                'Name': med_info['name'],
                'Category': med_info['category'],
                'Composition': ", ".join(med_info['composition']),
                'Reason': " ".join(list(dict.fromkeys(data['reasons']))),
                'score': data['score']
            })

    final_df = pd.DataFrame(reco_list).sort_values(by='score', ascending=False).head(5)
    return final_df.drop(columns=['score'])


# --- Streamlit UI ---
st.title("💊 Medicine Recommendation Search Engine")

if not medicines_data or not users_data:
    st.error("Could not load data. Please check the database connection and make sure it's populated.")
else:
    all_user_ids = sorted([u['_id'] for u in users_data])
    
    if not all_user_ids:
        st.error("Error: Could not find any users in the database! Please make sure your MongoDB server is running and that you have successfully run the `seed_db.py` script to populate the database.")
    else:
        # --- ⭐⭐⭐ FINAL UI LAYOUT CHANGE ⭐⭐⭐ ---
        
        selected_user = st.selectbox(
            "Select your user profile:",
            options=all_user_ids,
            format_func=lambda uid: f"{next((u['name'] for u in users_data if u['_id'] == uid), '')} ({uid})"
        )
        
        search_term = st.text_input(
            "Search by medicine name or symptom:", 
            placeholder="e.g., 'fever', 'Dolo', 'headache'"
        )

        if st.button("Get Recommendations"):
            with st.spinner("🧠 Analyzing your profile and finding the best recommendations..."):
                recommendations_df = get_recommendations(selected_user, search_term, medicines_data, users_data)
                
                if recommendations_df.empty:
                    st.warning("No relevant recommendations found. Please try a different search term.")
                else:
                    st.subheader("Here are your top recommendations:")
                    st.dataframe(recommendations_df, use_container_width=True, hide_index=True)

