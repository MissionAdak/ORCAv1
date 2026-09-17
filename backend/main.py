import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

# Import the existing app (now an APIRouter) from Sangeeta's services
from app import app as sangeeta_router
from data_ingestion import fetch_open_meteo_data, fetch_mock_incois_pfz, fetch_mock_alerts

app = FastAPI(title="ORCA API Gateway")

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Sangeeta's and Yug's existing services
app.include_router(sangeeta_router)

# ============================================================
# Database connection stub (Day 4)
# ============================================================
def get_available_data_sources(category: str):
    """
    Mock DB connection to data_source_registry.
    Filters available tide and lightning datasets.
    """
    db_url = os.getenv("DATABASE_URL")
    # Simulate DB lookup
    registry = [
        {
            "id": "uuid-tide-1",
            "source_name": "incois",
            "dataset_name": "tide_predictions",
            "category": "tide",
            "parameter": "tide_height",
            "update_frequency": "hourly",
            "authority_level": "official",
            "is_available": True
        },
        {
            "id": "uuid-lightning-1",
            "source_name": "imd",
            "dataset_name": "lightning_alerts",
            "category": "lightning",
            "parameter": "lightning_strike",
            "update_frequency": "real-time",
            "authority_level": "official",
            "is_available": True
        }
    ]
    return [source for source in registry if source["category"] == category and source["is_available"]]

# ============================================================
# API Gateway Shells
# ============================================================

@app.get("/api/marine/forecast")
def get_marine_forecast(lat: float, lon: float, date: str = None):
    """
    Day 3: Serve the normalized Open-Meteo data.
    """
    data = fetch_open_meteo_data(lat, lon)
    return {"status": "success", "data": data}

@app.get("/api/weather/forecast")
def get_weather_forecast(lat: float, lon: float, date: str = None):
    """
    Day 3: Serve normalized weather forecast data.
    """
    data = fetch_open_meteo_data(lat, lon)
    return {"status": "success", "data": data}

@app.get("/api/pfz/nearby")
def get_pfz_nearby(lat: float, lon: float, max_distance_km: Optional[float] = 50.0):
    """
    Day 3: Serve the mocked INCOIS PFZ polygons.
    """
    data = fetch_mock_incois_pfz(lat, lon)
    return {"status": "success", "data": data}

@app.get("/api/alerts/nearby")
def get_alerts_nearby(lat: float, lon: float, radius_km: Optional[float] = 50.0):
    """
    Day 3: Active hazard/cyclone/lightning alerts.
    """
    data = fetch_mock_alerts(lat, lon, radius_km)
    return {"status": "success", "alerts": data}

@app.get("/api/geospatial/zones")
def get_geospatial_zones(bbox: str):
    """
    Day 3: Hazard/restricted/IMBL polygons for map layer.
    """
    return {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [[72.0, 19.0], [73.0, 19.0], [73.0, 20.0], [72.0, 20.0], [72.0, 19.0]]
                    ]
                },
                "properties": {
                    "zone_type": "restricted",
                    "severity": "high"
                }
            }
        ]
    }

class ChatIntentRequest(BaseModel):
    intent_json: dict

@app.post("/api/chat")
def post_chat(request: ChatIntentRequest):
    """
    Day 3: Route the structured Bhashini intent JSON to Yug's orchestrator.
    """
    return {
        "status": "success",
        "message": "Intent routed to LangGraph orchestrator.",
        "received_intent": request.intent_json
    }

class FishingProductivityRequest(BaseModel):
    region: dict
    start_date: str
    end_date: str
    species: Optional[str] = None

@app.post("/api/trends/fishing-productivity")
def get_fishing_productivity(request: FishingProductivityRequest):
    """
    Day 4: Query historical SST, chlorophyll, and PFZ changes.
    """
    return {
        "status": "success",
        "trend_direction": "declining",
        "trend_metrics": {
            "sst_trend": "+0.5C",
            "chlorophyll_trend": "-1.2mg/m3",
            "pfz_frequency": "-15%"
        },
        "observed_changes": "The selected region shows a decline in PFZ frequency and chlorophyll concentration over the selected period, while SST increased.",
        "possible_contributing_factors": ["SST increase", "Current shifts"],
        "evidence": ["incois_historical", "mosdac_historical"],
        "confidence": 0.85
    }

@app.get("/api/data-sources/catalog")
def get_data_sources_catalog():
    """
    Shell for Data Sources Catalog.
    """
    tides = get_available_data_sources("tide")
    lightning = get_available_data_sources("lightning")
    return {"status": "success", "catalog": tides + lightning}

@app.get("/api/data-sources/status")
def get_data_sources_status():
    """
    Health/staleness of each ingestion source.
    """
    return {
        "status": "success",
        "sources": [
            {"source": "open-meteo", "status": "healthy", "last_updated": "2026-09-17T08:00:00Z"},
            {"source": "incois", "status": "healthy", "last_updated": "2026-09-17T08:00:00Z"}
        ]
    }

class SARCreateGatewayRequest(BaseModel):
    latitude: float
    longitude: float

@app.post("/api/sar/create")
def create_sar_incident_gateway(request: SARCreateGatewayRequest):
    """
    Gateway shell for SAR Create.
    """
    return {"status": "gateway shell not fully implemented"}
