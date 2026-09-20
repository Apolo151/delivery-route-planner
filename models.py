from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Delivery:
    """Represents a single delivery request."""
    id: int
    area: str
    priority: int
    weight: float

    def is_valid(self, max_capacity: float = 10.0) -> bool:
        """
        Validates if a package can theoretically be shipped.
        Edge Case: Package is heavier than the vehicle's capacity or has invalid weight.
        """
        return 0 < self.weight <= max_capacity


class Trip:
    """Represents a single vehicle's delivery route."""
    
    def __init__(self, max_capacity: float = 10.0):
        self.deliveries: List[Delivery] = []
        self.current_weight: float = 0.0
        self.max_capacity: float = max_capacity
        
        # Tracks the area of the first package loaded to encourage geographical grouping
        self.primary_area: Optional[str] = None

    def can_fit(self, delivery: Delivery) -> bool:
        """
        Edge Case Check: Adding the next package would exceed vehicle capacity.
        Returns True if the package fits in the remaining space.
        """
        # Using a small epsilon (like rounding to 2 decimals) prevents floating point errors
        # e.g., 9.999999999999998 > 10.0
        return round(self.current_weight + delivery.weight, 2) <= self.max_capacity

    def add_delivery(self, delivery: Delivery) -> None:
        """
        Adds a delivery to the trip, updating the total weight and primary area.
        """
        if not self.can_fit(delivery):
            raise ValueError(f"Cannot add delivery {delivery.id}: exceeds vehicle capacity.")
        
        self.deliveries.append(delivery)
        self.current_weight += delivery.weight
        
        # The primary area is dictated by the highest priority package (the first one added)
        if self.primary_area is None:
            self.primary_area = delivery.area