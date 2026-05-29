from datetime import datetime
from bson.objectid import ObjectId
from pymongo import MongoClient

db = MongoClient("mongodb://localhost:27017/")["restaurants"]
col = db["restaurants"]

def input_validated(prompt, min_len=None, exact_len=None, required=True):
    while True:
        val = input(prompt).strip()
        if required and not val:
            print("Dieses Feld ist ein Pflichtfeld!")
            continue
        if not required and not val:
            return ""
        if min_len and len(val) < min_len:
            print(f"Eingabe muss mindestens {min_len} Zeichen lang sein!")
            continue
        if exact_len and len(val) != exact_len:
            print(f"Eingabe muss exakt {exact_len} Zeichen lang sein!")
            continue
        return val

def bewertung_abgeben():
    search_name = input_validated("Nach welchem Restaurant suchst du? ", min_len=2)
    results = list(col.find({"name": {"$regex": search_name, "$options": "i"}}))
    
    if not results:
        print("Kein Restaurant gefunden.")
        return
        
    selected_restaurant = None
    if len(results) > 1:
        print(f"Es wurden {len(results)} Restaurants gefunden:")
        for idx, r in enumerate(results):
            print(f"[{idx}] {r.get('name')} ({r.get('borough')})")
        
        while True:
            try:
                choice = int(input("Wähle die Nummer des Restaurants aus: "))
                if 0 <= choice < len(results):
                    selected_restaurant = results[choice]
                    break
            except ValueError:
                pass
            print("Ungültige Auswahl!")
    else:
        selected_restaurant = results[0]
        
    doc_id = selected_restaurant["_id"]
    print(f"Ausgewähltes Restaurant ID: {doc_id}")
    
    try:
        score = int(input("Bewertung eingeben (z.B. 1-10): "))
    except ValueError:
        score = 5
        
    grade = input("Note/Buchstabe (z.B. A, B, C): ").upper() or "A"
    
    new_grade = {
        "date": datetime.now(),
        "grade": grade,
        "score": score
    }
    
    col.update_one({"_id": doc_id}, {"$push": {"grades": new_grade}})
    print("Bewertung erfolgreich hinzugefügt!")

def restaurant_hinzufuegen():
    print("\n--- Neues Restaurant hinzufügen ---")
    name = input_validated("Name: ", min_len=2)
    borough = input_validated("Borough: ", min_len=2)
    cuisine = input_validated("Cuisine: ", min_len=2)
    building = input_validated("Hausnummer (Optional): ", required=False)
    street = input_validated("Strasse: ", min_len=2)
    zipcode = input_validated("Postleitzahl (5-stellig): ", exact_len=5)
    
    new_doc = {
        "name": name,
        "borough": borough,
        "cuisine": cuisine,
        "address": {
            "building": building,
            "street": street,
            "zipcode": zipcode
        },
        "grades": []
    }
    
    col.insert_one(new_doc)
    print(f"Restaurant '{name}' wurde erfolgreich hinzugefügt!")

def restaurant_loeschen():
    print("\n--- Restaurants löschen ---")
    search_name = input_validated("Name (oder Teil) des zu löschenden Restaurants: ", min_len=2)
    
    query = {"name": {"$regex": search_name, "$options": "i"}}
    count = col.count_documents(query)
    
    if count == 0:
        print("Es wurden keine passenden Restaurants gefunden.")
        return
        
    print(f"Es wurden {count} Restaurants gefunden.")
    confirm = input(f"Möchtest du diese {count} Restaurants wirklich löschen? (ja/nein): ").strip().lower()
    
    if confirm == "ja":
        col.delete_many(query)
        print(f"Es wurden {count} Restaurants erfolgreich gelöscht.")
    else:
        print("Löschvorgang abgebrochen.")

if __name__ == "__main__":
    while True:
        print("\n=== RESTAURANT APP ===")
        print("1: Restaurant bewerten")
        print("2: Restaurant hinzufügen")
        print("3: Restaurants löschen")
        print("4: Beenden")
        
        wahl = input("Auswahl treffen: ").strip()
        if wahl == "1":
            bewertung_abgeben()
        elif wahl == "2":
            restaurant_hinzufuegen()
        elif wahl == "3":
            restaurant_loeschen()
        elif wahl == "4":
            break