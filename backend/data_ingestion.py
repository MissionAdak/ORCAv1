from datetime import datetime, timezone

def fetch_mock_open_meteo_data(lat: float, lon: float) -> dict:
    """
    Mock fetching data from Open-Meteo and strictly formatting it into the 
    ORCA Standard Data Model defined in the PRD.
    """
    return {
        "source": "open-meteo",
        "parameter": "wave_height",
        "value": 1.42,
        "unit": "m",
        "latitude": lat,
        "longitude": lon,
        "valid_time": datetime.now(timezone.utc).isoformat(),
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "confidence": 0.82,
        "is_stale": False,
        "conflict_flag": False
    }
