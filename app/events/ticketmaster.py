import requests
import os

# Hole den API Key aus den Umgebungsvariablen
API_KEY = os.environ.get('TICKETMASTER_API_KEY')
BASE_URL = "https://app.ticketmaster.com/discovery/v2/events.json"

def fetch_events(keyword=None, city=None, start_date=None, end_date=None):
    API_KEY = os.environ.get('TICKETMASTER_API_KEY')
    if not API_KEY or API_KEY == "DUMMY":
        # Dummy-Daten für Tests
        return [
            {
                "title": "Test Event",
                "start": "2025-01-01T20:00:00Z",
                "location": "Test Location",
                "city": "Berlin",
                "country": "DE",
                "url": "https://example.com",
                "artists": "Test Artist"
            }
        ]

    params = {
        "apikey": API_KEY,
        "countryCode": "DE",
        "classificationName": "music",
        "keyword": keyword,
        "city": city,
        "startDateTime": start_date,
        "endDateTime": end_date
    }
    filtered_params = {k: v for k, v in params.items() if v}
    response = requests.get(BASE_URL, params=filtered_params)
    if response.status_code != 200:
        raise Exception(f"Ticketmaster API error: {response.status_code} - {response.text}")

    events = response.json().get("_embedded", {}).get("events", [])
    structured_events = []

    for event in events:
        event_data = {
            "title": event.get("name", "No title available"),
            "start": event.get("dates", {}).get("start", {}).get("localDate", "No date available"),
            "location": event.get("_embedded", {}).get("venues", [{}])[0].get("name", "No venue available"),
            "city": event.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name", "No city available"),
            "country": event.get("_embedded", {}).get("venues", [{}])[0].get("country", {}).get("name", "No country available"),
            "url": event.get("url", "No URL available")
        }

        # Füge den Künstlernamen hinzu, falls vorhanden
        if "attractions" in event:
            artists = [artist.get("name") for artist in event["attractions"]]
            event_data["artists"] = ", ".join(artists) if artists else "No artist available"

        structured_events.append(event_data)

    return structured_events