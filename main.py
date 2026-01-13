from utils.file_handler import read_sales_data
from utils.data_processor import (
    parse_transactions,
    validate_and_filter,
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
    try:
        print("=" * 35)
        print("SALES ANALYTICS SYSTEM")
        print("=" * 35)

        print("\n[1/10] Reading sales data...")
        raw_lines = read_sales_data("data/sales_data.txt")
        print(f"✓ Successfully read {len(raw_lines)} transactions")

        print("\n[2/10] Parsing and cleaning data...")
        transactions = parse_transactions(raw_lines)
        print(f"✓ Parsed {len(transactions)} records")

        print("\n[3/10] Filter Options Available:")
        regions = sorted(set(tx["region"] for tx in transactions))
        amounts = [tx["quantity"] * tx["unit_price"] for tx in transactions]
        print(f"Regions: {', '.join(regions)}")
        print(f"Amount Range: ₹{min(amounts):,.0f} - ₹{max(amounts):,.0f}")

        choice = input("\nDo you want to filter data? (y/n): ").strip().lower()

        region = None
        min_amt = None
        max_amt = None

        if choice == "y":
            region = input("Enter region (or press Enter to skip): ").strip() or None
            min_amt = input("Enter minimum amount (or press Enter to skip): ").strip()
            max_amt = input("Enter maximum amount (or press Enter to skip): ").strip()

            min_amt = float(min_amt) if min_amt else None
            max_amt = float(max_amt) if max_amt else None

        print("\n[4/10] Validating transactions...")
        valid_tx, invalid_count, summary = validate_and_filter(
            transactions, region, min_amt, max_amt
        )
        print(f"✓ Valid: {len(valid_tx)} | Invalid: {invalid_count}")

        print("\n[5/10] Analyzing sales data...")
        calculate_total_revenue(valid_tx)
        region_wise_sales(valid_tx)
        top_selling_products(valid_tx)
        customer_analysis(valid_tx)
        daily_sales_trend(valid_tx)
        find_peak_sales_day(valid_tx)
        low_performing_products(valid_tx)
        print("✓ Analysis complete")

        print("\n[6/10] Fetching product data from API...")
        api_products = fetch_all_products()
        product_mapping = create_product_mapping(api_products)

        print("\n[7/10] Enriching sales data...")
        enriched_transactions = enrich_sales_data(valid_tx, product_mapping)
        matched = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
        print(f"✓ Enriched {matched}/{len(enriched_transactions)} transactions")

        print("\n[8/10] Saving enriched data...")
        save_enriched_data(enriched_transactions)

        print("\n[9/10] Generating report...")
        generate_sales_report(valid_tx, enriched_transactions)

        print("\n[10/10] Process Complete!")
        print("=" * 35)

    except Exception as e:
        print("❌ An error occurred:", str(e))


if __name__ == "__main__":
    main()
