from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import phonenumbers
from phonenumbers import geocoder, carrier
from geopy.geocoders import OpenCage

app = FastAPI()

# Tambahkan Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Bisa disesuaikan, misalnya ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key (Pastikan ini valid)
GOOGLE_MAPS_API_KEY = "AIzaSyDTVWCQ2rFL8XVQMq-lfEYQ2bi46ebw-Os"
OPENCAGE_API_KEY = "d32ab2639b33497997924f8e27d51da4"

class PhoneRequest(BaseModel):
    phone_number: str

@app.post("/track")
def track_number(request: PhoneRequest):
    phone_number = request.phone_number.strip()

    if not phone_number.startswith("+62"):
        return {"error": "Nomor harus dari Indonesia (+62)"}

    # Parsing nomor HP
    parsed_number = phonenumbers.parse(phone_number)
    location = geocoder.description_for_number(parsed_number, "id")
    provider = carrier.name_for_number(parsed_number, "id")

    # Dapatkan koordinat dengan OpenCage
    geolocator = OpenCage(api_key=OPENCAGE_API_KEY)
    location_data = geolocator.geocode(location)

    if location_data:
        latitude = location_data.latitude
        longitude = location_data.longitude
    else:
        return {"error": "Lokasi tidak ditemukan"}

    google_maps_url = f"https://www.google.com/maps/embed/v1/place?key={GOOGLE_MAPS_API_KEY}&q={latitude},{longitude}"

    return {
        "phone_number": phone_number,
        "location": location,
        "provider": provider,
        "latitude": latitude,
        "longitude": longitude,
        "google_maps_url": google_maps_url
    }

# Jalankan server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)