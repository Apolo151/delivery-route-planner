import sys
from parser import DeliveryParser
from planner import RoutePlanner

def print_summary_statistics(trips, unshippable):
    """
    Extension Feature: Trip Summary Statistics
    Prints a high-level overview of routing efficiency for dispatchers.
    """
    print("\n" + "="*50)
    print("📊 TRIP SUMMARY STATISTICS (EXTENSION)")
    print("="*50)
    
    total_trips = len(trips)
    if total_trips == 0:
        print("No valid trips were generated.")
        return

    total_weight = sum(trip.current_weight for trip in trips)
    avg_weight = total_weight / total_trips
    max_capacity = 10.0  # Vehicle limit
    utilization = (avg_weight / max_capacity) * 100

    print(f"Total Trips Generated     : {total_trips}")
    print(f"Total Weight Delivered    : {total_weight:.2f} kg")
    print(f"Average Fleet Utilization : {utilization:.1f}% capacity per vehicle")
    
    if unshippable:
        print(f"⚠️ Unshippable Packages   : {len(unshippable)} (Exceeds capacity)")
    else:
        print(f"✅ All packages successfully routed.")
    print("="*50 + "\n")

def main():
    # Require the filepath as a command line argument
    if len(sys.argv) < 2:
        print("Usage: python main.py <path_to_json_file>")
        sys.exit(1)

    filepath = sys.argv[1]

    # 1. Parse Input
    parser = DeliveryParser()
    deliveries = parser.load_from_csv(filepath)

    if not deliveries:
        print("No deliveries to process. Exiting cleanly.")
        sys.exit(0)

    # 2. Plan Routes
    planner = RoutePlanner()
    # process_deliveries returns our packed trips and any packages > 10kg
    trips, unshippable = planner.process_deliveries(deliveries)

    # 3. Output Results (Dispatch Manifest)
    print("\n" + "="*50)
    print("🚚 DISPATCH MANIFEST")
    print("="*50)
    for i, trip in enumerate(trips, 1):
        print(f"\nTrip #{i} | Primary Area: {trip.primary_area} | Total Weight: {trip.current_weight:.2f}kg")
        print("-" * 50)
        for d in trip.deliveries:
            print(f"  [Priority {d.priority}] ID: {d.id} | Area: {d.area} | Weight: {d.weight}kg")

    if unshippable:
        print("\n" + "="*50)
        print("❌ UNSHIPPABLE DELIVERIES (> 10kg limit)")
        print("="*50)
        for d in unshippable:
             print(f"  ID: {d.id} | Weight: {d.weight}kg | Area: {d.area}")

    # 4. Execute custom extension feature
    print_summary_statistics(trips, unshippable)

if __name__ == "__main__":
    main()
