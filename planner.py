
from typing import List, Tuple
from models import Delivery, Trip

class RoutePlanner:
    """Core logic for organizing deliveries into optimized trips using a First-Fit heuristic."""
    
    def __init__(self, max_capacity: float = 10.0):
        self.max_capacity = max_capacity
        
    def process_deliveries(self, deliveries: List[Delivery]) -> Tuple[List[Trip], List[Delivery]]:
        trips: List[Trip] = []
        unshippable: List[Delivery] = []
        
        # Edge Case 1: There are no deliveries
        if not deliveries:
            return trips, unshippable
            
        valid_deliveries: List[Delivery] = []
        
        # Edge Case 2: A package is heavier than the vehicle's capacity (10 kg)
        # We separate these out so they don't crash the routing loop.
        for d in deliveries:
            if d.is_valid(self.max_capacity):
                valid_deliveries.append(d)
            else:
                unshippable.append(d)
                
        # Edge Case 3: Multiple deliveries have the same priority
        # By sorting with a tuple (priority, area), we guarantee that if priorities are equal,
        # packages for the same area are processed sequentially. This maximizes grouping.
        valid_deliveries.sort(key=lambda x: (x.priority, x.area, -x.weight))
        
        # Core Routing Loop (Bin Packing)
        for delivery in valid_deliveries:
            placed = False
            
            # Rule: Deliveries going to the same area should be grouped together.
            # Edge Case 4: Adding the next package would exceed vehicle capacity (handled by trip.can_fit).
            for trip in trips:
                if trip.primary_area == delivery.area and trip.can_fit(delivery):
                    trip.add_delivery(delivery)
                    placed = True
                    break
                    
            # Design Decision: If no existing trip for this area has space, create a NEW trip.
            # We strictly isolate areas (e.g., we do not put a Maadi package in a Zamalek vehicle
            # just because there is leftover weight). This reflects real-world logistics efficiency.
            if not placed:
                new_trip = Trip(max_capacity=self.max_capacity)
                new_trip.add_delivery(delivery)
                trips.append(new_trip)
                
        return trips, unshippable
