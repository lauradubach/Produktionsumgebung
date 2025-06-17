import os
import requests

API_KEY = os.getenv("TICKETMASTER_API_KEY")

# Holt ein einzelnes Event anhand der Event-ID
def fetch_event_by_id(event_id):
    url = f"https://app.ticketmaster.com/discovery/v2/events/{event_id}.json"
    params = {"apikey": API_KEY}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        return {
            "id": data.get("id"),
            "title": data.get("name"),
            "start": data.get("dates", {}).get("start", {}).get("dateTime"),
            "location": data.get("_embedded", {}).get("venues", [{}])[0].get("name"),
            "city": data.get("_embedded", {}).get("venues", [{}])[0].get("city", {}).get("name"),
            "country": data.get("_embedded", {}).get("venues", [{}])[0].get("country", {}).get("name"),
            "url": data.get("url"),
            "artists": ", ".join(
                [a.get("name") for a in data.get("_embedded", {}).get("attractions", [])]
            ) if "_embedded" in data and "attractions" in data["_embedded"] else ""
        }

    except requests.RequestException as e:
        print(f"Fehler beim Abrufen des Events {event_id}: {e}")
        return None


# Sucht mehrere Events per Keyword
def fetch_events(keyword=None, city=None, country_codes=None, start_date=None, end_date=None):
    import os
    import requests

    base_url = "https://app.ticketmaster.com/discovery/v2/events.json"
    params = {
        "apikey": API_KEY,
        "classificationName": "music",
        "size": 20,
    }

    if keyword:
        params["keyword"] = keyword
    if city:
        params["city"] = city
    if country_codes:
        params["countryCode"] = country_codes
    if start_date:
        params["startDateTime"] = start_date + "T00:00:00Z"
    if end_date:
        params["endDateTime"] = end_date + "T23:59:59Z"

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        events = data.get("_embedded", {}).get("events", [])

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
                "artists": ", ".join([
                    a.get("name") for a in e.get("_embedded", {}).get("attractions", [])
                ]) if "_embedded" in e and "attractions" in e["_embedded"] else ""
            })
        return simplified

    except requests.RequestException as e:
        print(f"Fehler beim Abrufen der Events: {e}")
        return []