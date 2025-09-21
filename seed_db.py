import csv
import json
from pymongo import MongoClient

# --- Connection to MongoDB ---
client = MongoClient('mongodb://localhost:27017/')
db = client['medicine_reco']
medicines_collection = db.medicines
users_collection = db.users

print("Dropping old collections if they exist...")
medicines_collection.drop()
users_collection.drop()

# --- Seed Medicines from CSV ---
print("Seeding medicines...")
with open('medicines.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        # We split the simple string from the CSV back into a proper list
        composition_list = row['composition'].split(';')
        
        medicines_collection.insert_one({
            '_id': row['_id'],
            'name': row['name'],
            'composition': composition_list, # Now it's a perfect list!
            'category': row['category'],
            'price': float(row['price'])
        })

# --- Seed Users from JSON ---
print("Seeding users...")
with open('users.json', 'r') as f:
    users_data = json.load(f)
    users_collection.insert_many(users_data)

print("Database seeding complete!")
    

