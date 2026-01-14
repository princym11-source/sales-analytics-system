from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter_transactions,
    calculate_total_revenue,
    region_wise_sales,
    top_selling_products,
    customer_analysis,
    daily_sales_trend,
    find_peak_sales_day,
    low_performing_products,
    generate_sales_report
)
from utils.api_handler import (
    fetch_all_products,
    create_product_mapping,
    enrich_sales_data,
    save_enriched_data
)


def main():
    print("=" * 40)
    print("SALES ANALYTICS SYSTEM")
    print("=" * 40)

    # Step 1: Read data
    print("\nReading sales data...")
    raw_lines = read_sales_data("data/sales_data.txt")

    # Step 2: Parse data
    print("Parsing transactions...")
    transactions = parse_transactions(raw_lines)

    # Step 3: Validate data
    print("Validating transactions...")
    valid_tx = validate_and_filter_transactions(transactions)
    print(f"Valid transactions: {len(valid_tx)}")

    # Step 4: Analysis
    print("Running analysis...")
    calculate_total_revenue(valid_tx)
    region_wise_sales(valid_tx)
    top_selling_products(valid_tx)
    customer_analysis(valid_tx)
    daily_sales_trend(valid_tx)
    find_peak_sales_day(valid_tx)
    low_performing_products(valid_tx)

    # Step 5: API integration
    print("Fetching product data from API...")
    api_products = fetch_all_products()
    product_mapping = create_product_mapping(api_products)

    # Step 6: Enrich data
    print("Enriching sales data...")
    enriched_transactions = enrich_sales_data(valid_tx, product_mapping)
    save_enriched_data(enriched_transactions)

    # Step 7: Generate report
    print("Generating sales report...")
    generate_sales_report(valid_tx, enriched_transactions)

    print("\nProcess completed successfully!")


if __name__ == "__main__":
    main()
