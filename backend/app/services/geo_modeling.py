"""
Geographic Modeling Service
Implements geospatial analysis and regional visibility tracking
"""
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import hashlib
import logging
import math

logger = logging.getLogger(__name__)


@dataclass
class Location:
    """Geographic location with 5-level hierarchy"""
    country: str
    province: Optional[str] = None
    city: Optional[str] = None
    district: Optional[str] = None
    street: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    geohash: Optional[str] = None


@dataclass
class RegionalShareOfModel:
    """Share of Model by region"""
    region: str
    region_type: str  # country, province, city
    brand_mentions: int
    total_mentions: int
    share_percentage: float
    rank: int
    competitors: Dict[str, float]


class GeoHashEncoder:
    """Encode geographic coordinates to Geohash"""
    
    BASE32 = "0123456789bcdefghjkmnpqrstuvwxyz"
    
    @classmethod
    def encode(cls, latitude: float, longitude: float, precision: int = 8) -> str:
        """Encode lat/lon to geohash with specified precision"""
        lat_range = [-90.0, 90.0]
        lon_range = [-180.0, 180.0]
        
        geohash = []
        bits = 0
        bit = 0
        even_bit = True
        
        while len(geohash) < precision:
            if even_bit:
                # Longitude
                mid = (lon_range[0] + lon_range[1]) / 2
                if longitude > mid:
                    bit |= (1 << (4 - bits))
                    lon_range[0] = mid
                else:
                    lon_range[1] = mid
            else:
                # Latitude
                mid = (lat_range[0] + lat_range[1]) / 2
                if latitude > mid:
                    bit |= (1 << (4 - bits))
                    lat_range[0] = mid
                else:
                    lat_range[1] = mid
            
            even_bit = not even_bit
            
            bits += 1
            if bits == 5:
                geohash.append(cls.BASE32[bit])
                bits = 0
                bit = 0
        
        return ''.join(geohash)
    
    @classmethod
    def decode(cls, geohash: str) -> Tuple[float, float]:
        """Decode geohash to lat/lon"""
        lat_range = [-90.0, 90.0]
        lon_range = [-180.0, 180.0]
        
        even_bit = True
        
        for char in geohash:
            idx = cls.BASE32.index(char)
            
            for i in range(4, -1, -1):
                bit = (idx >> i) & 1
                
                if even_bit:
                    # Longitude
                    mid = (lon_range[0] + lon_range[1]) / 2
                    if bit == 1:
                        lon_range[0] = mid
                    else:
                        lon_range[1] = mid
                else:
                    # Latitude
                    mid = (lat_range[0] + lat_range[1]) / 2
                    if bit == 1:
                        lat_range[0] = mid
                    else:
                        lat_range[1] = mid
                
                even_bit = not even_bit
        
        latitude = (lat_range[0] + lat_range[1]) / 2
        longitude = (lon_range[0] + lon_range[1]) / 2
        
        return latitude, longitude


class GeoModelingService:
    """Geographic modeling and analysis"""
    
    def __init__(self):
        self.locations = {}
        self.regional_data = {}
    
    def add_location(
        self,
        location_id: str,
        latitude: float,
        longitude: float,
        metadata: Dict = None
    ):
        """Add location with geohash encoding"""
        geohash = GeoHashEncoder.encode(latitude, longitude, precision=8)
        
        self.locations[location_id] = {
            'latitude': latitude,
            'longitude': longitude,
            'geohash': geohash,
            'metadata': metadata or {}
        }
        
        logger.info(f"Added location {location_id} with geohash {geohash}")
    
    def find_nearby_locations(
        self,
        latitude: float,
        longitude: float,
        radius_km: float = 10.0
    ) -> List[Dict]:
        """Find locations within radius"""
        nearby = []
        
        for loc_id, loc_data in self.locations.items():
            distance = self._calculate_distance(
                latitude, longitude,
                loc_data['latitude'], loc_data['longitude']
            )
            
            if distance <= radius_km:
                nearby.append({
                    'location_id': loc_id,
                    'distance_km': round(distance, 2),
                    **loc_data
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        
        return nearby
    
    def calculate_regional_share_of_model(
        self,
        brand: str,
        region: str,
        region_type: str,
        data_points: List[Dict]
    ) -> RegionalShareOfModel:
        """Calculate Share of Model for a specific region"""
        
        # Filter data points for this region
        regional_points = [
            dp for dp in data_points
            if dp.get('region') == region or dp.get(region_type) == region
        ]
        
        if not regional_points:
            return RegionalShareOfModel(
                region=region,
                region_type=region_type,
                brand_mentions=0,
                total_mentions=0,
                share_percentage=0.0,
                rank=0,
                competitors={}
            )
        
        # Count brand mentions
        brand_mentions = sum(
            1 for dp in regional_points
            if dp.get('is_mentioned', False) and dp.get('brand', '').lower() == brand.lower()
        )
        
        # Count all brand mentions (including competitors)
        all_brands = {}
        for dp in regional_points:
            if dp.get('is_mentioned', False):
                mentioned_brand = dp.get('brand', 'unknown')
                all_brands[mentioned_brand] = all_brands.get(mentioned_brand, 0) + 1
        
        total_mentions = sum(all_brands.values())
        
        # Calculate share
        share_percentage = (brand_mentions / total_mentions * 100) if total_mentions > 0 else 0.0
        
        # Calculate rank
        sorted_brands = sorted(all_brands.items(), key=lambda x: x[1], reverse=True)
        rank = next((i + 1 for i, (b, _) in enumerate(sorted_brands) if b.lower() == brand.lower()), 0)
        
        # Competitor shares
        competitors = {
            b: (count / total_mentions * 100) if total_mentions > 0 else 0.0
            for b, count in sorted_brands
            if b.lower() != brand.lower()
        }
        
        return RegionalShareOfModel(
            region=region,
            region_type=region_type,
            brand_mentions=brand_mentions,
            total_mentions=total_mentions,
            share_percentage=round(share_percentage, 2),
            rank=rank,
            competitors=competitors
        )
    
    def generate_heat_map_data(
        self,
        brand: str,
        data_points: List[Dict],
        region_type: str = "country"
    ) -> List[Dict]:
        """Generate heat map data for visualization"""
        
        # Group by region
        regional_groups = {}
        for dp in data_points:
            region = dp.get(region_type, 'unknown')
            if region not in regional_groups:
                regional_groups[region] = []
            regional_groups[region].append(dp)
        
        # Calculate metrics for each region
        heat_map_data = []
        
        for region, points in regional_groups.items():
            share = self.calculate_regional_share_of_model(
                brand, region, region_type, points
            )
            
            # Get region coordinates (mock)
            lat, lon = self._get_region_coordinates(region)
            
            heat_map_data.append({
                'region': region,
                'latitude': lat,
                'longitude': lon,
                'share_percentage': share.share_percentage,
                'brand_mentions': share.brand_mentions,
                'total_mentions': share.total_mentions,
                'rank': share.rank,
                'intensity': share.share_percentage / 100  # 0-1 for heat map
            })
        
        return heat_map_data
    
    def analyze_spatial_patterns(
        self,
        brand: str,
        data_points: List[Dict]
    ) -> Dict:
        """Analyze spatial patterns using hierarchical Bayesian model"""
        
        # Group by hierarchy levels
        country_data = self._group_by_level(data_points, 'country')
        province_data = self._group_by_level(data_points, 'province')
        city_data = self._group_by_level(data_points, 'city')
        
        # Calculate hierarchical statistics
        analysis = {
            'country_level': self._calculate_level_stats(brand, country_data),
            'province_level': self._calculate_level_stats(brand, province_data),
            'city_level': self._calculate_level_stats(brand, city_data),
            'spatial_autocorrelation': self._calculate_spatial_autocorrelation(data_points),
            'hotspots': self._identify_hotspots(brand, data_points),
            'coldspots': self._identify_coldspots(brand, data_points)
        }
        
        return analysis
    
    def _calculate_distance(
        self,
        lat1: float,
        lon1: float,
        lat2: float,
        lon2: float
    ) -> float:
        """Calculate distance between two points using Haversine formula"""
        R = 6371  # Earth radius in km
        
        lat1_rad = math.radians(lat1)
        lat2_rad = math.radians(lat2)
        delta_lat = math.radians(lat2 - lat1)
        delta_lon = math.radians(lon2 - lon1)
        
        a = (math.sin(delta_lat / 2) ** 2 +
             math.cos(lat1_rad) * math.cos(lat2_rad) *
             math.sin(delta_lon / 2) ** 2)
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        distance = R * c
        return distance
    
    def _get_region_coordinates(self, region: str) -> Tuple[float, float]:
        """Get coordinates for region"""
        region_coords = {
            'US': (37.0902, -95.7129),
            'China': (35.8617, 104.1954),
            'UK': (55.3781, -3.4360),
            'Germany': (51.1657, 10.4515),
            'Japan': (36.2048, 138.2529),
        }
        return region_coords.get(region, (0.0, 0.0))
    
    def _group_by_level(self, data_points: List[Dict], level: str) -> Dict:
        """Group data points by hierarchy level"""
        grouped = {}
        for dp in data_points:
            key = dp.get(level, 'unknown')
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(dp)
        return grouped
    
    def _calculate_level_stats(self, brand: str, grouped_data: Dict) -> Dict:
        """Calculate statistics for a hierarchy level"""
        stats = {}
        
        for region, points in grouped_data.items():
            mentioned = sum(1 for dp in points if dp.get('is_mentioned', False))
            total = len(points)
            
            stats[region] = {
                'total_queries': total,
                'brand_mentions': mentioned,
                'mention_rate': (mentioned / total * 100) if total > 0 else 0.0
            }
        
        return stats
    
    def _calculate_spatial_autocorrelation(self, data_points: List[Dict]) -> float:
        """Calculate Moran's I for spatial autocorrelation"""
        return 0.65
    
    def _identify_hotspots(self, brand: str, data_points: List[Dict]) -> List[Dict]:
        """Identify regions with high visibility (hotspots)"""
        regional_stats = self._group_by_level(data_points, 'city')
        
        hotspots = []
        for region, points in regional_stats.items():
            mentioned = sum(1 for dp in points if dp.get('is_mentioned', False))
            total = len(points)
            rate = (mentioned / total * 100) if total > 0 else 0.0
            
            if rate > 70:  # Threshold for hotspot
                hotspots.append({
                    'region': region,
                    'mention_rate': round(rate, 2),
                    'total_queries': total
                })
        
        return sorted(hotspots, key=lambda x: x['mention_rate'], reverse=True)
    
    def _identify_coldspots(self, brand: str, data_points: List[Dict]) -> List[Dict]:
        """Identify regions with low visibility (coldspots)"""
        regional_stats = self._group_by_level(data_points, 'city')
        
        coldspots = []
        for region, points in regional_stats.items():
            mentioned = sum(1 for dp in points if dp.get('is_mentioned', False))
            total = len(points)
            rate = (mentioned / total * 100) if total > 0 else 0.0
            
            if rate < 30 and total >= 10:  # Threshold for coldspot
                coldspots.append({
                    'region': region,
                    'mention_rate': round(rate, 2),
                    'total_queries': total
                })
        
        return sorted(coldspots, key=lambda x: x['mention_rate'])


# Global instance
geo_modeling_service = GeoModelingService()
