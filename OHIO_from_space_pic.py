import requests
import os
from math import radians, cos, sin, acos




def is_over_ohio(lat, lon, center_lat=40.19, center_lon=-82.67, max_km=300):
    r = 6371  # Earth's radius in km
    lat1, lon1 = radians(lat), radians(lon)
    lat2, lon2 = radians(center_lat), radians(center_lon)
    d = acos(sin(lat1)*sin(lat2) + cos(lat1)*cos(lat2)*cos(lon1 - lon2)) * r
    return d <= max_km

def auto_download_earth_image_over_ohio():
    NASA_API_KEY = "DEMO_KEY"  # Replace with your NASA API Key if you have one
    base_url = "https://api.nasa.gov/EPIC/api/natural"
    save_path = "./space_images/earth_over_ohio.jpg"

    try:
        response = requests.get(f"{base_url}?api_key={NASA_API_KEY}")
        response.raise_for_status()
        metadata = response.json()
    except Exception as e:
        print(f"[JARVIS] Failed to contact NASA EPIC API: {e}")
        return

    for item in metadata:
        coords = item.get("centroid_coordinates", {})
        lat, lon = coords.get("lat"), coords.get("lon")
        if lat is not None and is_over_ohio(lat, lon):
            date = item["date"].split()[0].replace("-", "/")
            img_name = item["image"]
            img_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date}/jpg/{img_name}.jpg"
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            try:
                img_data = requests.get(img_url).content
                with open(save_path, "wb") as f:
                    f.write(img_data)
                print(f"[JARVIS] Auto-downloaded Earth image over Ohio ({item['date']})")
                return
            except Exception as e:
                print(f"[JARVIS] Could not download image: {e}")
                return

    print("[JARVIS] No recent EPIC image over Ohio.")


