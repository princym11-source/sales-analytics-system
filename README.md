Sales Analytics System
📌 Project Overview

This project is a Python-based Sales Analytics System developed as part of Module 3 – Python Programming Assignment.
The system processes raw sales transaction data, cleans and validates it, performs multiple levels of analysis, integrates external API data, and generates a comprehensive sales report.

The project demonstrates concepts such as:

File handling with encoding support

Data cleaning and validation

Data analysis using lists and dictionaries

API integration

Report generation

Modular and structured Python programming

📂 Project Structure
sales-analytics-system/
│
├── main.py
├── README.md
├── requirements.txt
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt
│
└── utils/
    ├── file_handler.py
    ├── data_processor.py
    └── api_handler.py

⚙️ Features Implemented
Part 1: File Handling & Preprocessing

Reads sales data with encoding handling

Parses and cleans messy transaction records

Handles commas in text and numeric fields

Validates records and applies optional filters

Part 2: Data Processing

Calculates total revenue

Region-wise sales analysis

Top selling products

Customer purchase analysis

Daily sales trends and peak sales day

Low performing product identification

Part 3: API Integration

Fetches product data from DummyJSON API

Creates product ID mapping

Enriches sales data with API details

Saves enriched data to file

Part 4: Report Generation

Generates a detailed text-based sales report

Includes summaries, tables, trends, and API enrichment insights

Part 5: Main Application

Executes the complete workflow

Provides user interaction for filtering

Handles errors gracefully

Displays progress messages

▶️ How to Run the Project
1️⃣ Install Dependencies

Make sure Python is installed, then run:

pip install -r requirements.txt

2️⃣ Run the Application

From the root project directory:

python main.py

📄 Output Files

After successful execution:

Enriched Sales Data:
data/enriched_sales_data.txt

Sales Report:
output/sales_report.txt

🧪 API Used

DummyJSON Products API
https://dummyjson.com/products

✅ Notes

The repository is public as required.

All files follow the prescribed folder structure.

The application runs end-to-end without errors.

Output files are generated automatically.

👤 Author
Princy Mishra
