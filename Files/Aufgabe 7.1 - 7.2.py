import os
import gridfs
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["photo_album_db"]
fs = gridfs.GridFS(db)

def foto_hinzufuegen():
    album = input("Name des Albums: ").strip()
    path = input("Pfad zum Foto (z.B. bild.jpg): ").strip()
    
    if not os.path.exists(path):
        print("Datei nicht gefunden!")
        return
        
    filename = os.path.basename(path)
    
    with open(path, "rb") as f:
        fs.put(f, filename=filename, metadata={"album": album})
        
    print(f"Foto '{filename}' wurde dem Album '{album}' hinzugefügt.")

def fotos_herunterladen():
    album = input("Welches Album möchtest du herunterladen?: ").strip()
    
    files = list(db["fs.files"].find({"metadata.album": album}))
    
    if not files:
        print("Keine Fotos in diesem Album gefunden.")
        return
        
    os.makedirs(album, exist_ok=True)
    
    for file_doc in files:
        file_id = file_doc["_id"]
        filename = file_doc["filename"]
        
        grid_out = fs.get(file_id)
        output_path = os.path.join(album, filename)
        
        with open(output_path, "wb") as f:
            f.write(grid_out.read())
            
        print(f"Heruntergeladen: {output_path}")

if __name__ == "__main__":
    while True:
        print("\n=== FOTOALBUM APP ===")
        print("1: Foto hinzufügen")
        print("2: Album herunterladen")
        print("3: Beenden")
        
        wahl = input("Auswahl: ").strip()
        if wahl == "1":
            foto_hinzufuegen()
        elif wahl == "2":
            fotos_herunterladen()
        elif wahl == "3":
            break