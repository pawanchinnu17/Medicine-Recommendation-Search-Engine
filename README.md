# 💊 Intelligent Medicine Recommendation Search Engine

This project brings to life an intelligent, web-based search engine that acts as a smart pharmacist's assistant. It moves beyond simple keyword matching to provide users with **personalized and relevant medicine recommendations**.  

The core mission is to create a system that understands a user's needs—whether they're searching for a specific product, describing a symptom like `"acidity"`, or simply looking for a reminder of what they usually buy.

The result is a fully functional **web application** with a clean, interactive interface that showcases a **sophisticated, multi-layered recommendation logic**, all powered by a robust and flexible database backend.

---

## ⚙️ Our Project Approach: How It Works

Our goal was to create a smart, personalized pharmacist's assistant. This required a thoughtful approach to connect our data, logic, and user interface into a single, intelligent system.

### 1️⃣ The Foundation: Realistic Data  
A recommendation engine is only as good as its data. Since real-world purchase history is private, we built a **Data Factory** (`generate_data.py`) to create high-quality, synthetic data.  
- We designed specific **user personas** (e.g., *Pain & Cold*, *Digestive*, *Chronic*) that mimic realistic shopping behaviors.  
- This ensures our recommendations remain logical and meaningful.  

### 2️⃣ The Memory: Flexible Storage with MongoDB  
We chose **MongoDB** as our database for its flexibility.  
- A user's purchase history is a **list that grows over time**.  
- MongoDB’s document model naturally stores this within a single record.  
- This makes it more efficient and scalable than a traditional SQL database for user-centric applications.  

### 3️⃣ The Bridge: Automated Setup  
We built a **simple, two-step process** to make the data live:  
1. `generate_data.py` → creates raw data files  
2. `seed_db.py` → loads them into MongoDB  

This ensures a **clean, repeatable setup** for anyone running the project.  

### 4️⃣ The Brain: Live Data & Multi-Layered Logic  
The core logic resides in **`app.py`**.  
When a user searches for a medicine, the app pulls **live data from MongoDB** and applies a **multi-layered scoring system**:  
- **Direct Match** → Does the medicine match the search term or symptom?  
- **Personalization** → Has this user bought it before?  
- **Collaborative Filtering** → What have similar users purchased?  

### 5️⃣ The Face: A Simple Interface with Streamlit  
We used **Streamlit** to build the user interface.  
- It allowed us to rapidly create a **clean, interactive web app** entirely in Python.  
- Streamlit acts as both **frontend and backend**, making the system lightweight and easy to deploy.  

---

### 📊 The Foundation: High-Quality, Realistic Data  

A recommendation engine is only as smart as its data. Since real-world medical data is private, our project's foundation is a **high-quality synthetic dataset** created by the `generate_data.py` script. This script produces two essential files:  

#### 1️⃣ `medicines.csv` – The Pharmacy Catalog  
This file acts as our **complete list of available medicines**. Each row is a unique product with details like:  
- **Name** → The brand name (e.g., *Crocin Advance*)  
- **Composition** → The active ingredients (e.g., *Paracetamol*)  
- **Category** → The medical classification (e.g., *Analgesic*)  

#### 2️⃣ `users.json` – The Customer Profiles  
This file contains the **detailed profiles of users**.  
The key to our engine's accuracy lies in the `purchase_history` for each user, crafted around logical user personas:  

- **🩺 Pain & Cold Persona** → Users with purchase histories full of **painkillers, allergy pills, and cough syrups**.  
- **🍽️ Digestive Persona** → Users focused on **antacids and digestive wellness products**.  
- **♾️ Chronic Persona** → Users regularly buying medicines for **long-term conditions** like diabetes or hypertension.  

✅ This **persona-driven approach** ensures the data is **clean, logical, and realistic**, which is the secret to making the engine’s recommendations feel accurate and genuinely helpful.  

---

## 🛠️ Tech Stack

| Icon | Technology | Role |
|------|------------|------|
| 🐍 | **Python** | Core language for application logic, data generation, and DB interaction |
| 🎈 | **Streamlit** | Framework for building the interactive web app |
| 🍃 | **MongoDB** | NoSQL database for flexible user profiles & purchase history |
| 🐼 | **Pandas** | Efficient data handling and manipulation |
| 🍃 | **PyMongo** | Connects Python with MongoDB to insert and query user profiles & purchase histories |


---

## 📸 Application Demonstration

1. **Symptom-Based Search**  
   - Searching `"fever"` returns relevant medicines from the *Analgesic* category using the built-in symptom dictionary.  
   <img width="1812" height="762" alt="image" src="https://github.com/user-attachments/assets/2ea7f4a7-6630-4012-b2ee-0c3b2a877e7b" />



2. **Personalized Recommendations (Empty Search)**  
   - If the search bar is empty, the engine defaults to **personalized mode**, suggesting medicines based on the user’s past purchases.  
   <img width="1775" height="774" alt="image" src="https://github.com/user-attachments/assets/af2fe0f9-2172-4ce8-9a7b-96f59138b613" />


3. **Multi-Layered Logic in Action**  
   - A user with a *Digestive* profile searches for `"fever"`.  
   - Results show:  
     ✅ Direct matches  
     ✅ Past purchase preferences  
     ✅ Collaborative filtering ("Others with similar taste")  
   <img width="1810" height="793" alt="image" src="https://github.com/user-attachments/assets/347250cc-cfaa-448f-b043-8e2c67af3af8" />


---

## 🗄️ Architectural Choice: Why MongoDB?

MongoDB was chosen over SQL databases like MySQL because of its **flexible document model**, which makes it a perfect fit for storing user profiles and purchase histories.  

- A SQL database is like a **library** with rigid card catalogs. Storing a user’s purchase history (which can grow indefinitely) is complex.  
- MongoDB is like a **filing cabinet**—each user has a folder where all their info (including shopping history) is stored together.  

✅ More **intuitive**  
✅ More **flexible**  
✅ Faster for retrieving complete user profiles  

---

## 🎯 Summary

The Intelligent Medicine Recommendation Engine is more than a search tool,it’s a personalized pharmacist assistant powered by:

Symptom mapping

Purchase history

Collaborative filtering
