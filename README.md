# Delivery Route Planner

The Delivery Route Planner is a lightweight Python command-line application designed to organize CSV delivery manifests into optimized vehicle trips. 

It implements a modified First-Fit Decreasing (FFD) heuristic, utilizing a three-tier sorting mechanism (Priority, Area, Weight) to ensure that:
- Vehicle capacity never exceeds the 10 kg limit.
- Deliveries are processed strictly by urgency (Priority 1 being the highest).
- Packages are strictly grouped by geographical area to reflect realistic, efficient driver routes.
- Fleet capacity is dynamically optimized by packing the heaviest items first within their respective geographic clusters.

This tool was built using Python's `dataclasses` and standard libraries to prioritize code clarity, robust data validation, and ease of testing. It also features a built-in Trip Summary Statistics dashboard to provide immediate visibility into fleet utilization.

## File Structure
```text
delivery-route-planner/
├── main.py             # Entry point, orchestration, and CLI output
├── models.py           # Data structures (Delivery and Trip definitions)
├── parser.py           # File I/O, JSON parsing, and data validation
├── planner.py          # Core routing algorithm and edge-case handling
├── data/
│   └── deliveries.csv # Sample input data 
└── README.md           # Documentation and assignment reasoning

```

## Local Setup

### Prerequisites

* Python 3.8 or higher installed on your system.
* No external packages (like `pandas` or `numpy`) are required. The application relies entirely on the Python standard library.

### Installation & Execution

1. **Clone or Extract the Repository:**
Open your terminal and navigate to the project directory:
```bash
cd delivery-route-planner

```


2. **(Optional) Create a Virtual Environment:**
While there are no external dependencies, using a virtual environment is a Python best practice:
```bash
python3 -m venv venv
source venv/bin/activate

```


3. **Run the Application:**
Execute the `main.py` script and pass the path to the JSON data file as an argument:
```bash
python3 main.py data/deliveries.csv

```

### Input Data Format

The application expects a CSV file (`data/deliveries.csv`) with the following headers.
*(Note: I chose CSV over JSON because tabular data is the industry standard for logistics. The parser explicitly casts and validates these strings into proper data types, making the application robust against malformed data).*

```csv
ID,Area,Priority,Package Weight (kg)
1,Nasr City,2,4.5
2,Maadi,1,2.0
```

## Solution Approach

### 1. Explain your solution approach in your own words.

My solution uses a modified First-Fit Decreasing (FFD) heuristic, adapted for geographic constraints.

- First, the parser reads the CSV and filters out invalid deliveries (like packages > 10kg). 
- Second, it sorts the data on three levels: first by Priority (ascending, to respect urgency), then by Area (alphabetical, for geographic clustering), and finally by Weight (descending, heaviest first).

Finally, it iterates through the sorted list and attempts to pack each package into an existing trip that matches its Area and has enough remaining capacity. If no such trip exists, it opens a new trip. I made a strict design decision to isolate areas, the algorithm will not mix packages from different areas in the same vehicle just to maximize the 10kg limit. By feeding the heaviest packages first, the algorithm naturally optimizes fleet capacity by placing bulky items into empty trucks and plugging the remaining weight gaps with smaller packages.

### 2. What was the most difficult part of the assignment?

The most difficult part was balancing the trade-off between fleet efficiency (maximizing the 10kg capacity) and real-world business logic (geography and urgency). A pure mathematical bin-packing algorithm would aggressively mix packages from different neighborhoods just to reach 10kg, which is a terrible experience for a driver.

I had to design a sorting mechanism that respected the business rules first without completely sacrificing vehicle capacity. Implementing the three-tier sort (priority, area, -weight) solved this.

### 3. Are there situations where your algorithm may not produce the best possible grouping? Explain.

Yes. Because this algorithm strictly isolates geographical areas, it will sometimes sacrifice total fleet efficiency to keep routes segregated.

For example, if we have:

- Maadi: One package weighing 1kg.

- Zamalek: One package weighing 9kg.

An optimal mathematical algorithm (like a global 0/1 Knapsack) aiming purely for weight efficiency would put both of these into a single 10kg vehicle to save a trip.

My algorithm explicitly forbids this. It will generate two separate trips—one for Maadi and one for Zamalek. While this is mathematically "suboptimal" in terms of vehicle count and weight capacity, I chose this constraint because, in real-world logistics, sending a single driver across a city to deliver a 1kg package on the back of a 9kg route creates severe time delays that outweigh the vehicle savings.

### 4. If the input contained 1,000,000 delivery requests, what part of your solution might become slow or memory-intensive?

The algorithm itself sorts in O(N log N) time, which scales well. However, the **memory footprint** would become the bottleneck. Currently, `parser.py` will load all 1,000,000 rows into RAM as instantiated `Delivery` objects before processing them.
To fix this, I would implement **chunking or streaming**. Instead of loading the entire file into memory, the system would ingest the CSV in chunks, persist them to an indexed database, and execute the routing logic via optimized queries.

### 5. What would you improve if you had another day to work on the solution?

If I had another day, I would improve two things:

1. **Dynamic Programming:** I would try implementing a 0/1 Knapsack algorithm to mathematically optimize the capacity of the vehicles rather than relying on a greedy heuristic.
2. **Unit Testing:** I would write a `pytest` suite to programmatically verify the edge cases (empty files, same priority, exceeding capacity) without relying purely on manual CLI execution.

## Extra Feature

**Trip Summary Statistics Dashboard**
I implemented a post-processing summary dashboard that prints at the end of the routing run.

* **Why:** In real-world logistics, dispatchers don't just need the routes; they need immediate visibility into fleet efficiency and anomalies. This feature calculates total trips, total weight, average vehicle capacity utilization (%), and alerts the team to any un-routable packages (e.g., those exceeding the 10kg limit).