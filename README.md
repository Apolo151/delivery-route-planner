# Delivery Route Planner

The Delivery Route Planner is a lightweight, zero-dependency Python command-line application designed to organize delivery requests into optimized trips. 

It implements a modified first-fit bin-packing algorithm to ensure that:
- Vehicle capacity never exceeds the 10 kg limit.
- Deliveries are processed strictly by urgency (Priority 1 being the highest).
- Packages destined for the same area are grouped together within the same trip whenever mathematically possible.

This tool was built using Python's `dataclasses` and standard libraries to prioritize code clarity, readability, and ease of testing.

## File Structure
```text
delivery-route-planner/
├── main.py             # Entry point, orchestration, and CLI output
├── models.py           # Data structures (Delivery and Trip definitions)
├── parser.py           # File I/O, JSON parsing, and data validation
├── planner.py          # Core routing algorithm and edge-case handling
├── data/
│   └── deliveries.json # Sample input data
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
python3 main.py data/deliveries.json

```



### Expected Output (TBD)

The program will print a formatted list of generated trips to standard output, displaying the total weight and the specific packages assigned to each trip.

```

```