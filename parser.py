import csv
import sys
import os
from typing import List
from models import Delivery

class DeliveryParser:
    """Handles the ingestion and validation of CSV delivery data."""
    
    @staticmethod
    def load_from_csv(filepath: str) -> List[Delivery]:
        if not os.path.exists(filepath):
            print(f"Error: The file '{filepath}' does not exist.")
            sys.exit(1)

        deliveries = []
        
        try:
            with open(filepath, mode='r', encoding='utf-8-sig') as file:
                reader = csv.DictReader(file)
                
                # Check for empty file or missing headers
                if not reader.fieldnames:
                    print("Warning: The input CSV file is empty or missing headers.")
                    return []
                    
                for row_num, row in enumerate(reader, start=2): # start=2 accounts for header
                    try:
                        # Explicit casting acts as our data validation layer
                        delivery = Delivery(
                            id=int(row['ID'].strip()),
                            area=row['Area'].strip(),
                            priority=int(row['Priority'].strip()),
                            weight=float(row['Package Weight (kg)'].strip())
                        )
                        deliveries.append(delivery)
                        
                    except KeyError as e:
                        print(f"Warning: Missing expected column {e} in row {row_num}. Skipping.")
                    except ValueError:
                        print(f"Warning: Invalid data type (e.g., non-numeric weight/priority) in row {row_num}. Skipping.")
                        
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            sys.exit(1)

        return deliveries
