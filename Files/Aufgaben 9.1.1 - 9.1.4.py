import random
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["jukebox_db"]
col = db["songs"]

class Song:
    def __init__(self, name, interpret, album="", genre="", year=""):
        self.name = name
        self.interpret = interpret
        self.album = album
        self.genre = genre
        self.year = year

def song_hinzufuegen():
    name = input("Name (Pflichtfeld): ").strip()
    interpret = input("Interpret (Pflichtfeld): ").strip()
    if not name or not interpret:
        print("Name und Interpret dürfen nicht leer sein!")
        return
    album = input("Album (Optional): ").strip()
    genre = input("Genre (Optional): ").strip()
    year = input("Erscheinungsjahr (Optional): ").strip()
    
    neuer_song = Song(name, interpret, album, genre, year)
    col.insert_one(neuer_song.__dict__)
    print("Song erfolgreich hinzugefügt.")

def song_suchen_und_waehlen():
    suchbegriff = input("Nach welchem Song suchst du? ").strip()
    query = {
        "$or": [
            {"name": {"$regex": suchbegriff, "$options": "i"}},
            {"interpret": {"$regex": suchbegriff, "$options": "i"}}
        ]
    }
    results = list(col.find(query))
    if not results:
        print("Keine Songs gefunden.")
        return None
        
    for idx, s in enumerate(results):
        print(f"[{idx}] {s.get('name')} - {s.get('interpret')}")
        
    try:
        wahl = int(input("Wähle die Nummer des Songs: "))
        if 0 <= wahl < len(results):
            return results[wahl]
    except ValueError:
        pass
    print("Ungültige Auswahl.")
    return None

def song_aendern():
    song = song_suchen_und_waehlen()
    if not song:
        return
        
    print("Gib neue Werte ein (leer lassen, um alten Wert zu behalten):")
    name = input(f"Neuer Name ({song['name']}): ").strip() or song['name']
    interpret = input(f"Neuer Interpret ({song['interpret']}): ").strip() or song['interpret']
    album = input(f"Neues Album ({song['album']}): ").strip() or song['album']
    genre = input(f"Neues Genre ({song['genre']}): ").strip() or song['genre']
    year = input(f"Neues Jahr ({song['year']}): ").strip() or song['year']
    
    col.update_one(
        {"_id": song["_id"]},
        {"$set": {"name": name, "interpret": interpret, "album": album, "genre": genre, "year": year}}
    )
    print("Song erfolgreich geändert.")

def song_loeschen():
    song = song_suchen_und_waehlen()
    if song:
        col.delete_one({"_id": song["_id"]})
        print("Song erfolgreich gelöscht.")