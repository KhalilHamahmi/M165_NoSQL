from pymongo import MongoClient
from PIL import Image, ImageDraw

client = MongoClient("mongodb://localhost:27017/")
db = client["restaurants"]
col = db["neighborhoods"]

def get_all_polygons():
    polygons = []
    for doc in col.find():
        geo = doc.get("geometry", {})
        if geo.get("type") == "Polygon":
            polygons.append(geo["coordinates"][0])
        elif geo.get("type") == "MultiPolygon":
            for poly in geo["coordinates"]:
                polygons.append(poly[0])
    return polygons

def scale_coords(polygons, width=800, height=800):
    all_lng = [pt[0] for poly in polygons for pt in poly]
    all_lat = [pt[1] for poly in polygons for pt in poly]
    
    if not all_lng or not all_lat:
        return []
        
    min_lng, max_lng = min(all_lng), max(all_lng)
    min_lat, max_lat = min(all_lat), max(all_lat)
    
    lng_side = max_lng - min_lng if max_lng != min_lng else 1
    lat_side = max_lat - min_lat if max_lat != min_lat else 1
    
    scaled_polygons = []
    for poly in polygons:
        scaled_poly = []
        for pt in poly:
            x = int((pt[0] - min_lng) / lng_side * (width - 40)) + 20
            y = height - int((pt[1] - min_lat) / lat_side * (height - 40)) - 20
            scaled_poly.append((x, y))
        scaled_polygons.append(scaled_poly)
    return scaled_polygons

def zeichne_einzelnes_polygon(scaled):
    im = Image.new(mode="RGB", size=(800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    if scaled:
        for i in range(len(scaled[0]) - 1):
            draw.line((scaled[0][i], scaled[0][i+1]), fill=(255, 0, 0), width=2)
    im.show()

def zeichne_alle_polygone_linien(scaled):
    im = Image.new(mode="RGB", size=(800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    for poly in scaled:
        for i in range(len(poly) - 1):
            draw.line((poly[i], poly[i+1]), fill=(0, 0, 255), width=1)
    im.show()

def zeichne_alle_polygone_ausgefuellt(scaled):
    im = Image.new(mode="RGB", size=(800, 800), color=(255, 255, 255))
    draw = ImageDraw.Draw(im)
    for poly in scaled:
        if len(poly) >= 3:
            draw.polygon(poly, fill=(200, 220, 255), outline=(0, 0, 255))
    im.show()

if __name__ == "__main__":
    raw_polygons = get_all_polygons()
    if not raw_polygons:
        print("Keine Daten gefunden.")
    else:
        scaled = scale_coords(raw_polygons)
        print("1: Einzelnes Polygon als Linie (8.1)")
        print("2: Alle Polygone als Linien (8.2)")
        print("3: Alle Polygone ausgefüllt (8.3)")
        wahl = input("Auswahl: ").strip()
        
        if wahl == "1":
            zeichne_einzelnes_polygon(scaled)
        elif wahl == "2":
            zeichne_alle_polygone_linien(scaled)
        elif wahl == "3":
            zeichne_alle_polygone_ausgefuellt(scaled)