"""
Store & NAP Management API Endpoints

Provides endpoints for managing store locations and NAP (Name, Address, Phone) consistency.
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.services.store_nap_management import (
    StoreNAPManager,
    Store,
    NAPConsistency
)

router = APIRouter()
nap_manager = StoreNAPManager()


# Request/Response Models
class StoreCreateRequest(BaseModel):
    """Request model for creating a store"""
    name: str = Field(..., description="Store name")
    address: str = Field(..., description="Store address")
    phone: str = Field(..., description="Store phone number")
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    hours: Optional[str] = Field(None, description="Business hours")
    website: Optional[str] = Field(None, description="Website URL")
    categories: List[str] = Field(default_factory=list, description="Business categories")


class StoreUpdateRequest(BaseModel):
    """Request model for updating a store"""
    name: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    latitude: Optional[float] = Field(None, ge=-90, le=90)
    longitude: Optional[float] = Field(None, ge=-180, le=180)
    hours: Optional[str] = None
    website: Optional[str] = None
    categories: Optional[List[str]] = None


class StoreResponse(BaseModel):
    """Response model for store data"""
    store_id: str
    name: str
    address: str
    phone: str
    latitude: float
    longitude: float
    hours: Optional[str]
    website: Optional[str]
    categories: List[str]
    created_at: datetime
    updated_at: datetime


class NAPConsistencyResponse(BaseModel):
    """Response model for NAP consistency check"""
    store_id: str
    consistency_score: float
    issues: List[Dict[str, Any]]
    platform_data: Dict[str, Dict[str, str]]
    recommendations: List[str]
    checked_at: datetime


class SchemaGenerationResponse(BaseModel):
    """Response model for Schema.org generation"""
    store_id: str
    schema_type: str
    json_ld: Dict[str, Any]
    generated_at: datetime


@router.post("/stores", response_model=StoreResponse, status_code=201)
async def create_store(request: StoreCreateRequest):
    """
    Create a new store location
    
    Creates a new store with NAP information and geographic coordinates.
    """
    try:
        store = Store(
            store_id=f"store_{datetime.utcnow().timestamp()}",
            name=request.name,
            address=request.address,
            phone=request.phone,
            latitude=request.latitude,
            longitude=request.longitude,
            hours=request.hours,
            website=request.website,
            categories=request.categories,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # In production, save to database
        # For now, return the created store
        
        return StoreResponse(
            store_id=store.store_id,
            name=store.name,
            address=store.address,
            phone=store.phone,
            latitude=store.latitude,
            longitude=store.longitude,
            hours=store.hours,
            website=store.website,
            categories=store.categories,
            created_at=store.created_at,
            updated_at=store.updated_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create store: {str(e)}")


@router.get("/stores/{store_id}", response_model=StoreResponse)
async def get_store(store_id: str):
    """
    Get store information by ID
    
    Retrieves detailed information about a specific store.
    """
    # In production, fetch from database
    # For now, return mock data
    return StoreResponse(
        store_id=store_id,
        name="Example Store",
        address="123 Main St, City, State 12345",
        phone="+1-555-0123",
        latitude=40.7128,
        longitude=-74.0060,
        hours="Mon-Fri 9:00-18:00",
        website="https://example.com",
        categories=["Restaurant", "Cafe"],
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )


@router.put("/stores/{store_id}", response_model=StoreResponse)
async def update_store(store_id: str, request: StoreUpdateRequest):
    """
    Update store information
    
    Updates NAP and other information for an existing store.
    """
    try:
        # In production, fetch existing store and update
        # For now, return updated mock data
        return StoreResponse(
            store_id=store_id,
            name=request.name or "Example Store",
            address=request.address or "123 Main St, City, State 12345",
            phone=request.phone or "+1-555-0123",
            latitude=request.latitude or 40.7128,
            longitude=request.longitude or -74.0060,
            hours=request.hours,
            website=request.website,
            categories=request.categories or ["Restaurant"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update store: {str(e)}")


@router.delete("/stores/{store_id}", status_code=204)
async def delete_store(store_id: str):
    """
    Delete a store
    
    Removes a store from the system.
    """
    # In production, delete from database
    return None


@router.get("/stores", response_model=List[StoreResponse])
async def list_stores(
    limit: int = Query(50, ge=1, le=100, description="Maximum number of stores to return"),
    offset: int = Query(0, ge=0, description="Number of stores to skip")
):
    """
    List all stores
    
    Returns a paginated list of all stores in the system.
    """
    # In production, fetch from database with pagination
    # For now, return mock data
    return [
        StoreResponse(
            store_id=f"store_{i}",
            name=f"Store {i}",
            address=f"{i} Main St, City, State 12345",
            phone=f"+1-555-{i:04d}",
            latitude=40.7128 + i * 0.01,
            longitude=-74.0060 + i * 0.01,
            hours="Mon-Fri 9:00-18:00",
            website=f"https://store{i}.example.com",
            categories=["Restaurant"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        for i in range(offset, min(offset + limit, offset + 5))
    ]


@router.get("/stores/{store_id}/nap-consistency", response_model=NAPConsistencyResponse)
async def check_nap_consistency(
    store_id: str,
    platforms: Optional[List[str]] = Query(None, description="Platforms to check (e.g., google, yelp)")
):
    """
    Check NAP consistency across platforms
    
    Analyzes NAP information consistency across multiple platforms and provides
    recommendations for improvement.
    """
    try:
        # Create mock store for demonstration
        store = Store(
            store_id=store_id,
            name="Example Restaurant",
            address="123 Main St, New York, NY 10001",
            phone="+1-555-0123",
            latitude=40.7128,
            longitude=-74.0060,
            hours="Mon-Fri 9:00-18:00",
            website="https://example.com",
            categories=["Restaurant"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Check consistency
        platform_list = [Platform(p) for p in platforms] if platforms else None
        report = nap_manager.check_nap_consistency(store, platform_list)
        
        return NAPConsistencyResponse(
            store_id=store_id,
            consistency_score=report.consistency_score,
            issues=[
                {
                    "field": issue.field,
                    "platform": issue.platform.value,
                    "expected": issue.expected_value,
                    "actual": issue.actual_value,
                    "severity": issue.severity
                }
                for issue in report.issues
            ],
            platform_data={
                platform.value: data
                for platform, data in report.platform_data.items()
            },
            recommendations=report.recommendations,
            checked_at=report.checked_at
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to check NAP consistency: {str(e)}")


@router.post("/stores/{store_id}/schema", response_model=SchemaGenerationResponse)
async def generate_schema(store_id: str):
    """
    Generate Schema.org LocalBusiness markup
    
    Creates structured data markup for the store that can be embedded in web pages
    to improve search engine visibility.
    """
    try:
        # Create mock store for demonstration
        store = Store(
            store_id=store_id,
            name="Example Restaurant",
            address="123 Main St, New York, NY 10001",
            phone="+1-555-0123",
            latitude=40.7128,
            longitude=-74.0060,
            hours="Mon-Fri 9:00-18:00",
            website="https://example.com",
            categories=["Restaurant"],
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Generate schema
        schema = nap_manager.generate_local_business_schema(store)
        
        return SchemaGenerationResponse(
            store_id=store_id,
            schema_type="LocalBusiness",
            json_ld=schema,
            generated_at=datetime.utcnow()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate schema: {str(e)}")


@router.post("/stores/batch-check", response_model=List[NAPConsistencyResponse])
async def batch_check_consistency(
    store_ids: List[str] = Query(..., description="List of store IDs to check"),
    platforms: Optional[List[str]] = Query(None, description="Platforms to check")
):
    """
    Batch check NAP consistency for multiple stores
    
    Efficiently checks NAP consistency for multiple stores in a single request.
    """
    try:
        results = []
        for store_id in store_ids[:10]:  # Limit to 10 stores per batch
            # Create mock store
            store = Store(
                store_id=store_id,
                name=f"Store {store_id}",
                address="123 Main St, City, State 12345",
                phone="+1-555-0123",
                latitude=40.7128,
                longitude=-74.0060,
                hours="Mon-Fri 9:00-18:00",
                website="https://example.com",
                categories=["Restaurant"],
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            platform_list = [Platform(p) for p in platforms] if platforms else None
            report = nap_manager.check_nap_consistency(store, platform_list)
            
            results.append(NAPConsistencyResponse(
                store_id=store_id,
                consistency_score=report.consistency_score,
                issues=[
                    {
                        "field": issue.field,
                        "platform": issue.platform.value,
                        "expected": issue.expected_value,
                        "actual": issue.actual_value,
                        "severity": issue.severity
                    }
                    for issue in report.issues
                ],
                platform_data={
                    platform.value: data
                    for platform, data in report.platform_data.items()
                },
                recommendations=report.recommendations,
                checked_at=report.checked_at
            ))
        
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to batch check consistency: {str(e)}")
