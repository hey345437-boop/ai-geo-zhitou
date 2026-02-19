"""
Store & NAP Management
Manages store locations and NAP (Name, Address, Phone) consistency
"""
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class Store:
    """Store entity"""
    id: str
    name: str
    address: str
    phone: str
    latitude: float
    longitude: float
    city: str
    state: str
    country: str
    postal_code: str
    website: Optional[str] = None
    hours: Optional[Dict] = None
    created_at: datetime = None


@dataclass
class NAPConsistency:
    """NAP consistency check result"""
    store_id: str
    consistency_score: float
    issues: List[Dict]
    platforms_checked: List[str]
    last_checked: datetime


class StoreNAPManager:
    """Manage stores and NAP consistency"""
    
    def __init__(self):
        self.stores: Dict[str, Store] = {}
        self.nap_data: Dict[str, Dict] = {}  # platform -> store_id -> NAP data
    
    def add_store(
        self,
        store_id: str,
        name: str,
        address: str,
        phone: str,
        latitude: float,
        longitude: float,
        city: str,
        state: str,
        country: str,
        postal_code: str,
        website: Optional[str] = None,
        hours: Optional[Dict] = None
    ) -> Store:
        """Add a new store"""
        store = Store(
            id=store_id,
            name=name,
            address=address,
            phone=phone,
            latitude=latitude,
            longitude=longitude,
            city=city,
            state=state,
            country=country,
            postal_code=postal_code,
            website=website,
            hours=hours,
            created_at=datetime.now()
        )
        
        self.stores[store_id] = store
        logger.info(f"Added store: {store_id} - {name}")
        
        return store
    
    def check_nap_consistency(
        self,
        store_id: str,
        platforms: List[str] = None
    ) -> NAPConsistency:
        """
        Check NAP consistency across platforms
        
        Args:
            store_id: Store ID
            platforms: Platforms to check (Google, Yelp, Facebook, etc.)
        """
        store = self.stores.get(store_id)
        if not store:
            raise ValueError(f"Store {store_id} not found")
        
        if platforms is None:
            platforms = ["google", "yelp", "facebook", "bing", "apple_maps"]
        
        # Fetch NAP data from platforms (mock implementation)
        platform_data = {}
        for platform in platforms:
            platform_data[platform] = self._fetch_platform_nap(store_id, platform)
        
        # Compare NAP data
        issues = []
        
        # Check name consistency
        name_variations = set()
        for platform, data in platform_data.items():
            if data and data.get("name"):
                name_variations.add(data["name"].lower().strip())
        
        if len(name_variations) > 1:
            issues.append({
                "type": "name_inconsistency",
                "severity": "high",
                "description": f"Name varies across platforms: {name_variations}",
                "platforms": list(platform_data.keys())
            })
        
        # Check address consistency
        address_variations = set()
        for platform, data in platform_data.items():
            if data and data.get("address"):
                address_variations.add(data["address"].lower().strip())
        
        if len(address_variations) > 1:
            issues.append({
                "type": "address_inconsistency",
                "severity": "high",
                "description": f"Address varies across platforms",
                "platforms": list(platform_data.keys())
            })
        
        # Check phone consistency
        phone_variations = set()
        for platform, data in platform_data.items():
            if data and data.get("phone"):
                # Normalize phone number
                normalized = self._normalize_phone(data["phone"])
                phone_variations.add(normalized)
        
        if len(phone_variations) > 1:
            issues.append({
                "type": "phone_inconsistency",
                "severity": "medium",
                "description": f"Phone number varies across platforms",
                "platforms": list(platform_data.keys())
            })
        
        # Check for missing listings
        for platform in platforms:
            if platform not in platform_data or not platform_data[platform]:
                issues.append({
                    "type": "missing_listing",
                    "severity": "high",
                    "description": f"Store not found on {platform}",
                    "platform": platform
                })
        
        # Calculate consistency score
        max_issues = len(platforms) * 3  # 3 NAP fields per platform
        consistency_score = max(0, 100 - (len(issues) / max_issues * 100))
        
        return NAPConsistency(
            store_id=store_id,
            consistency_score=round(consistency_score, 2),
            issues=issues,
            platforms_checked=platforms,
            last_checked=datetime.now()
        )
    
    def generate_local_business_schema(self, store_id: str) -> Dict:
        """Generate Schema.org LocalBusiness JSON-LD"""
        store = self.stores.get(store_id)
        if not store:
            raise ValueError(f"Store {store_id} not found")
        
        schema = {
            "@context": "https://schema.org",
            "@type": "LocalBusiness",
            "name": store.name,
            "address": {
                "@type": "PostalAddress",
                "streetAddress": store.address,
                "addressLocality": store.city,
                "addressRegion": store.state,
                "postalCode": store.postal_code,
                "addressCountry": store.country
            },
            "telephone": store.phone,
            "geo": {
                "@type": "GeoCoordinates",
                "latitude": store.latitude,
                "longitude": store.longitude
            }
        }
        
        if store.website:
            schema["url"] = store.website
        
        if store.hours:
            schema["openingHoursSpecification"] = self._format_opening_hours(store.hours)
        
        return schema
    
    def get_multi_location_summary(self) -> Dict:
        """Get summary of all store locations"""
        if not self.stores:
            return {
                "total_stores": 0,
                "by_country": {},
                "by_state": {},
                "avg_consistency_score": 0.0
            }
        
        by_country = {}
        by_state = {}
        
        for store in self.stores.values():
            by_country[store.country] = by_country.get(store.country, 0) + 1
            by_state[store.state] = by_state.get(store.state, 0) + 1
        
        return {
            "total_stores": len(self.stores),
            "by_country": by_country,
            "by_state": by_state,
            "stores": [
                {
                    "id": s.id,
                    "name": s.name,
                    "city": s.city,
                    "state": s.state,
                    "country": s.country
                }
                for s in self.stores.values()
            ]
        }
    
    def _fetch_platform_nap(self, store_id: str, platform: str) -> Optional[Dict]:
        """Fetch NAP data from platform (mock implementation)"""
        store = self.stores.get(store_id)
        if not store:
            return None
        
        # Mock data with slight variations
        variations = {
            "google": {
                "name": store.name,
                "address": store.address,
                "phone": store.phone
            },
            "yelp": {
                "name": store.name,
                "address": store.address.replace("Street", "St"),
                "phone": store.phone
            },
            "facebook": {
                "name": store.name,
                "address": store.address,
                "phone": store.phone.replace("-", "")
            },
            "bing": {
                "name": store.name,
                "address": store.address,
                "phone": store.phone
            },
            "apple_maps": {
                "name": store.name,
                "address": store.address,
                "phone": store.phone
            }
        }
        
        return variations.get(platform)
    
    def _normalize_phone(self, phone: str) -> str:
        """Normalize phone number"""
        # Remove all non-digit characters
        return ''.join(c for c in phone if c.isdigit())
    
    def _format_opening_hours(self, hours: Dict) -> List[Dict]:
        """Format opening hours for Schema.org"""
        opening_hours = []
        
        for day, times in hours.items():
            if times:
                opening_hours.append({
                    "@type": "OpeningHoursSpecification",
                    "dayOfWeek": day.capitalize(),
                    "opens": times.get("open", "09:00"),
                    "closes": times.get("close", "17:00")
                })
        
        return opening_hours


# Global instance
store_nap_manager = StoreNAPManager()
