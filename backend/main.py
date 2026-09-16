from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Import the existing app (now an APIRouter) from Sangeeta's services
from app import app as sangeeta_router
from data_ingestion import fetch_mock_open_meteo_data

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
# API Gateway Shells
# ============================================================

@app.get("/api/marine/forecast")
def get_marine_forecast(lat: float, lon: float, date: str):
    """
    Shell for Marine Forecast.
    """
    # Mocking a fetch using the standard data model
    mock_data = fetch_mock_open_meteo_data(lat, lon)
    return {"status": "not implemented", "data": [mock_data]}

@app.get("/api/data-sources/catalog")
def get_data_sources_catalog():
    """
    Shell for Data Sources Catalog.
    """
    return {"status": "not implemented", "catalog": []}

class SARCreateGatewayRequest(BaseModel):
    latitude: float
    longitude: float

@app.post("/api/sar/create")
def create_sar_incident_gateway(request: SARCreateGatewayRequest):
    """
    Gateway shell for SAR Create.
    Delegates to the internal /api/internal/sar/create service if needed.
    """
    return {"status": "gateway shell not fully implemented"}
