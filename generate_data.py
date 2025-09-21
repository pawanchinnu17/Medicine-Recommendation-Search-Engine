import csv
import json
import random
from faker import Faker
import uuid

# --- A much larger, real-world inspired medicine list ---
# Researched popular medicines for common conditions in India
MEDICINE_DATA = {
    # Pain & Cold Persona Medicines
    'Analgesic': {
        'Crocin Advance': ['Paracetamol'],
        'Dolo 650': ['Paracetamol'],
        'Combiflam': ['Ibuprofen', 'Paracetamol'],
        'Sumo Tablet': ['Nimesulide', 'Paracetamol'],
        'Voveran SR': ['Diclofenac'],
    },
    'Antihistamine': {
        'Cetrizet': ['Cetirizine'],
        'Allegra 120': ['Fexofenadine'],
        'Avil 25': ['Pheniramine'],
    },
    'Antitussive/Expectorant': {
        'Benadryl Cough Syrup': ['Diphenhydramine', 'Ammonium Chloride'],
        'Grilinctus Syrup': ['Dextromethorphan', 'Chlorpheniramine'],
        'Ascoril LS Syrup': ['Ambroxol', 'Levosalbutamol', 'Guaifenesin'],
    },
    # Digestive Persona Medicines
    'Antacid': {
        'Digene Acidity & Gas Relief Gel': ['Magnesium Hydroxide', 'Simethicone', 'Magnesium Aluminium Silicate'],
        'Gelusil MPS': ['Aluminium Hydroxide', 'Magnesium Hydroxide', 'Simethicone'],
        'Eno Fruit Salt': ['Sodium Bicarbonate', 'Citric Acid'],
    },
    'Proton Pump Inhibitor': {
        'Pan 40': ['Pantoprazole'],
        'Omez D': ['Omeprazole', 'Domperidone'],
        'Rantac 150': ['Ranitidine'],
    },
    # Chronic (Diabetic) Persona Medicines
    'Antidiabetic': {
        'Glycomet 500 SR': ['Metformin'],
        'Janumet 50/500': ['Sitagliptin', 'Metformin'],
        'Amaryl M 1mg': ['Glimepiride', 'Metformin'],
        'Galvus Met 50/500': ['Vildagliptin', 'Metformin'],
    },
    # Chronic (Hypertensive) Persona Medicines
    'Antihypertensive': {
        'Amlong 5': ['Amlodipine'],
        'Telma 40': ['Telmisartan'],
        'Losar 50': ['Losartan'],
        'Metolar XR 50': ['Metoprolol Succinate'],
    },
    # General Antibiotics
    'Antibiotic': {
        'Azithral 500': ['Azithromycin'],
        'Augmentin 625 Duo': ['Amoxicillin', 'Clavulanic Acid'],
        'Moxikind CV 625': ['Amoxicillin', 'Clavulanic Acid'],
    },
    # Other Common Medicines
    'Statin': {
        'Atorva 10': ['Atorvastatin'],
    },
    'Vitamin': {
        'Neurobion Forte': ['Vitamin B Complex'],
        'Shelcal 500': ['Calcium', 'Vitamin D3'],
    }
}


def create_medicine_list():
    """Flattens the structured data into a list of medicine dictionaries."""
    medicines = []
    med_id_counter = 1
    for category, brands in MEDICINE_DATA.items():
        for brand_name, composition in brands.items():
            medicines.append({
                "_id": f"med_{med_id_counter:03}",
                "name": brand_name,
                "composition": composition,
                "category": category,
                "price": round(random.uniform(20.0, 500.0), 2)
            })
            med_id_counter += 1
    return medicines

def generate_personas(medicines_list, num_users=150):
    """Creates realistic user personas with logical purchase histories."""
    fake = Faker('en_IN')
    users = []
    
    # Define medicine pools for each persona
    pain_cold_pool = [m for m in medicines_list if m['category'] in ['Analgesic', 'Antihistamine', 'Antitussive/Expectorant', 'Antibiotic']]
    digestive_pool = [m for m in medicines_list if m['category'] in ['Antacid', 'Proton Pump Inhibitor']]
    diabetic_pool = [m for m in medicines_list if m['category'] == 'Antidiabetic']
    hypertensive_pool = [m for m in medicines_list if m['category'] == 'Antihypertensive']
    general_pool = [m for m in medicines_list if m['category'] in ['Statin', 'Vitamin']]

    persona_distribution = {
        'Pain & Cold': (0.4, pain_cold_pool),
        'Digestive': (0.25, digestive_pool),
        'Diabetic': (0.2, diabetic_pool),
        'Hypertensive': (0.15, hypertensive_pool),
    }

    user_id_counter = 1
    for persona_name, (weight, main_pool) in persona_distribution.items():
        num_persona_users = int(num_users * weight)
        for _ in range(num_persona_users):
            user_id = f"user_{user_id_counter:03}"
            
            purchases = []
            num_purchases = random.randint(10, 60)
            
            for _ in range(num_purchases):
                # 80% chance to buy from their main pool, 20% from general or a random painkiller
                if random.random() < 0.8:
                    med = random.choice(main_pool)
                else:
                    med = random.choice(general_pool + pain_cold_pool[:2]) # Add some general vitamins/painkillers
                
                purchases.append({
                    "medicine_id": med["_id"],
                    "name": med["name"],
                    "purchase_date": fake.date_time_this_year().isoformat()
                })

            users.append({
                "_id": user_id,
                "name": fake.name(),
                "persona": persona_name, # Add persona for easier testing
                "purchase_history": purchases
            })
            user_id_counter += 1
    
    return users

# --- Main Script Execution ---
if __name__ == "__main__":
    print("Generating new, expanded, and realistic dataset...")

    all_medicines = create_medicine_list()
    all_users = generate_personas(all_medicines, num_users=150)

    # --- Write Medicines to CSV ---
    print(f"Writing {len(all_medicines)} medicines to medicines.csv...")
    with open('medicines.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=["_id", "name", "composition", "category", "price"])
        writer.writeheader()
        for med in all_medicines:
            med_to_write = med.copy()
            med_to_write['composition'] = ";".join(med['composition'])
            writer.writerow(med_to_write)

    # --- Write Users to JSON ---
    print(f"Writing {len(all_users)} users to users.json...")
    with open('users.json', 'w') as f:
        json.dump(all_users, f, indent=2)

    print("\nData generation complete!")
    print("You now have a much larger and more realistic dataset.")

