import os
import requests

def fetch_events(keyword=None, city=None, start_date=None, end_date=None, country_codes=None):
    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": os.getenv("TICKETMASTER_API_KEY"),
        "keyword": keyword,
        "city": city,
        "startDateTime": f"{start_date}T00:00:00Z" if start_date else None,
        "endDateTime": f"{end_date}T23:59:59Z" if end_date else None,
        "countryCode": country_codes,
        "classificationName": "music",
        "size": 20
    }

    # Entferne None-Werte
    clean_params = {k: v for k, v in params.items() if v}

    try:
        response = requests.get(base_url, params=clean_params)
        response.raise_for_status()
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

        # Vereinfacht zurückgeben
        simplified = []
        for e in events:
            simplified.append({
                "id": e.get("id"),
                "title": e.get("name"),
                "start": e.get("dates", {}).get("start", {}).get("dateTime"),
                "location": e.get("_embedded", {}).get("venues", [{}])[0].get("name"),
                "city": e.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
                "country": e.get("_embedded", {}).get("venues", [{}])[0].get("country", {}).get("name"),
                "url": e.get("url"),
                "artists": ", ".join([a.get("name") for a in e.get("_embedded", {}).get("attractions", [])])
                    if "_embedded" in e and "attractions" in e["_embedded"] else ""
            })
        return simplified

    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Events: {e}")
        return []