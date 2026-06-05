playlist = []

def song_suchen_kombiniert():
    print("\n--- Erweiterte Suche (Felder leer lassen zum Ignorieren) ---")
    name = input("Name: ").strip()
    interpret = input("Interpret: ").strip()
    album = input("Album: ").strip()
    genre = input("Genre: ").strip()
    
    query = {}
    if name: query["name"] = {"$regex": name, "$options": "i"}
    if interpret: query["interpret"] = {"$regex": interpret, "$options": "i"}
    if album: query["album"] = {"$regex": album, "$options": "i"}
    if genre: query["genre"] = {"$regex": genre, "$options": "i"}
    
    results = list(col.find(query))
    if not results:
        print("Keine passenden Songs gefunden.")
        return
        
    for idx, s in enumerate(results):
        print(f"[{idx}] {s.get('name')} - {s.get('interpret')} (Album: {s.get('album')}, Genre: {s.get('genre')})")
        
    try:
        wahl = input("Nummer des Songs zur Playlist hinzufügen (Enter zum Abbrechen): ").strip()
        if wahl:
            idx = int(wahl)
            if 0 <= idx < len(results):
                playlist.append(results[idx])
                print(f"'{results[idx]['name']}' zur Playlist hinzugefügt.")
    except ValueError:
        print("Ungültige Eingabe.")

def playlist_abspielen():
    if not playlist:
        print("\nPlaylist ist leer. Zufälliger Song wird abgespielt:")
        alle_songs = list(col.find())
        if not alle_songs:
            print("Keine Songs in der Datenbank vorhanden.")
            return
        zufalls_song = random.choice(alle_songs)
        print(f"Spiele Zufallssong: {zufalls_song['name']} - {zufalls_song['interpret']}")
    else:
        print("\n--- Spiele Playlist ab (FIFO) ---")
        while playlist:
            aktueller_song = playlist.pop(0)
            print(f"Spiele jetzt: {aktueller_song['name']} - {aktueller_song['interpret']}")