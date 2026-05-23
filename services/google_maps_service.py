import os
import httpx
import json
import asyncio
from typing import List, Dict, Any

class GoogleMapsService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_MAPS_API_KEY")
        self.is_mock_mode = not bool(self.api_key)
        self.base_url = "https://maps.googleapis.com/maps/api"

    async def get_distance_matrix(self, origins: List[str], destinations: List[str]) -> Dict[str, Any]:
        """
        Fetch distance and duration between points.
        Uses mock data if no API key is provided.
        """
        if self.is_mock_mode:
            return self._mock_distance_matrix(origins, destinations)

        async with httpx.AsyncClient() as client:
            origins_str = "|".join(origins)
            dest_str = "|".join(destinations)
            url = f"{self.base_url}/distancematrix/json?origins={origins_str}&destinations={dest_str}&key={self.api_key}"
            
            response = await client.get(url)
            response.raise_for_status()
            return response.json()

    def _mock_distance_matrix(self, origins: List[str], destinations: List[str]) -> Dict[str, Any]:
        """
        Generate plausible mock distance data for testing without an API key.
        """
        rows = []
        for o in origins:
            elements = []
            for d in destinations:
                if o == d:
                    elements.append({"distance": {"value": 0}, "duration": {"value": 0}, "status": "OK"})
                else:
                    # Random distance between 2km and 15km
                    import random
                    dist = random.randint(2000, 15000)
                    dur = int(dist / (40 * 1000 / 3600)) # roughly 40 km/h
                    elements.append({"distance": {"value": dist}, "duration": {"value": dur}, "status": "OK"})
            rows.append({"elements": elements})
            
        return {"rows": rows, "status": "OK"}

google_maps_client = GoogleMapsService()
