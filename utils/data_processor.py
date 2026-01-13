def parse_transactions(raw_lines):
    """
    Parses raw transaction lines into structured dictionaries

    Input: list of raw strings
    Output: list of dictionaries
    """

    transactions = []

    for line in raw_lines:
        parts = line.split('|')

        # Skip lines that do not have exactly 8 fields
        if len(parts) != 8:
            continue

        transaction = {
            "transaction_id": parts[0].strip(),
            "date": parts[1].strip(),
            "product_id": parts[2].strip(),
            "product_name": parts[3].strip(),
            "quantity": parts[4].strip(),
            "unit_price": parts[5].strip(),
            "customer_id": parts[6].strip(),
            "region": parts[7].strip()
        }

        transactions.append(transaction)

    return transactions


def validate_and_filter_transactions(transactions):
    """
    Validates and cleans parsed transaction data

    Input: list of transaction dictionaries
    Output: list of valid and cleaned transactions
    """

    valid_transactions = []
    invalid_count = 0

    for tx in transactions:
        try:
            # Validate transaction ID
            if not tx["transaction_id"].startswith("T"):
                invalid_count += 1
                continue

            # Check mandatory fields
            if not tx["customer_id"] or not tx["region"]:
                invalid_count += 1
                continue

            # Clean numeric values
            quantity = int(tx["quantity"])
            unit_price = float(tx["unit_price"].replace(",", ""))

            # Validate numeric values
            if quantity <= 0 or unit_price <= 0:
                invalid_count += 1
                continue

            # Update cleaned values
            tx["quantity"] = quantity
            tx["unit_price"] = unit_price

            valid_transactions.append(tx)

        except:
            invalid_count += 1
            continue

    print(f"Total records processed: {len(transactions)}")
    print(f"Invalid records removed: {invalid_count}")
    print(f"Valid records remaining: {len(valid_transactions)}")

    return valid_transactions


def calculate_total_revenue(transactions):
    """
    Calculates total revenue from all transactions
    """

    total_revenue = 0.0

    for tx in transactions:
        total_revenue += tx["quantity"] * tx["unit_price"]

    return total_revenue


def region_wise_sales(transactions):
    """
    Analyzes sales by region
    """

    region_data = {}
    overall_sales = calculate_total_revenue(transactions)

    for tx in transactions:
        region = tx["region"]
        revenue = tx["quantity"] * tx["unit_price"]

        if region not in region_data:
            region_data[region] = {
                "total_sales": 0.0,
                "transaction_count": 0
            }

        region_data[region]["total_sales"] += revenue
        region_data[region]["transaction_count"] += 1

    # Add percentage and sort
    sorted_regions = dict(
        sorted(
            region_data.items(),
            key=lambda item: item[1]["total_sales"],
            reverse=True
        )
    )

    for region in sorted_regions:
        percentage = (sorted_regions[region]["total_sales"] / overall_sales) * 100
        sorted_regions[region]["percentage"] = round(percentage, 2)

    return sorted_regions


def top_selling_products(transactions, n=5):
    """
    Finds top n products by total quantity sold
    """

    product_data = {}

    for tx in transactions:
        product = tx["product_name"]
        quantity = tx["quantity"]
        revenue = quantity * tx["unit_price"]

        if product not in product_data:
            product_data[product] = {
                "quantity": 0,
                "revenue": 0.0
            }

        product_data[product]["quantity"] += quantity
        product_data[product]["revenue"] += revenue

    sorted_products = sorted(
        product_data.items(),
        key=lambda item: item[1]["quantity"],
        reverse=True
    )

    result = []
    for product, data in sorted_products[:n]:
        result.append((product, data["quantity"], data["revenue"]))

    return result


def customer_analysis(transactions):
    """
    Analyzes customer purchase patterns
    """

    customer_data = {}

    for tx in transactions:
        customer = tx["customer_id"]
        revenue = tx["quantity"] * tx["unit_price"]

        if customer not in customer_data:
            customer_data[customer] = {
                "total_spent": 0.0,
                "purchase_count": 0,
                "products_bought": set()
            }

        customer_data[customer]["total_spent"] += revenue
        customer_data[customer]["purchase_count"] += 1
        customer_data[customer]["products_bought"].add(tx["product_name"])

    # Prepare final structure
    final_data = {}

    for customer, data in customer_data.items():
        avg_value = data["total_spent"] / data["purchase_count"]

        final_data[customer] = {
            "total_spent": round(data["total_spent"], 2),
            "purchase_count": data["purchase_count"],
            "avg_order_value": round(avg_value, 2),
            "products_bought": list(data["products_bought"])
        }

    # Sort by total spent
    final_data = dict(
        sorted(
            final_data.items(),
            key=lambda item: item[1]["total_spent"],
            reverse=True
        )
    )

    return final_data


def daily_sales_trend(transactions):
    """
    Analyzes sales trends by date
    """

    daily_data = {}

    for tx in transactions:
        date = tx["date"]
        revenue = tx["quantity"] * tx["unit_price"]

        if date not in daily_data:
            daily_data[date] = {
                "revenue": 0.0,
                "transaction_count": 0,
                "customers": set()
            }

        daily_data[date]["revenue"] += revenue
        daily_data[date]["transaction_count"] += 1
        daily_data[date]["customers"].add(tx["customer_id"])

    # Prepare final sorted result
    final_data = {}

    for date in sorted(daily_data.keys()):
        final_data[date] = {
            "revenue": round(daily_data[date]["revenue"], 2),
            "transaction_count": daily_data[date]["transaction_count"],
            "unique_customers": len(daily_data[date]["customers"])
        }

    return final_data


def find_peak_sales_day(transactions):
    """
    Identifies the date with highest revenue
    """

    daily_summary = daily_sales_trend(transactions)

    peak_date = None
    max_revenue = 0.0
    transaction_count = 0

    for date, data in daily_summary.items():
        if data["revenue"] > max_revenue:
            max_revenue = data["revenue"]
            peak_date = date
            transaction_count = data["transaction_count"]

    return (peak_date, max_revenue, transaction_count)



def low_performing_products(transactions, threshold=10):
    """
    Identifies products with low sales
    """

    product_data = {}

    for tx in transactions:
        product = tx["product_name"]
        quantity = tx["quantity"]
        revenue = quantity * tx["unit_price"]

        if product not in product_data:
            product_data[product] = {
                "total_quantity": 0,
                "total_revenue": 0.0
            }

        product_data[product]["total_quantity"] += quantity
        product_data[product]["total_revenue"] += revenue

    low_performers = []

    for product, data in product_data.items():
        if data["total_quantity"] < threshold:
            low_performers.append(
                (product, data["total_quantity"], data["total_revenue"])
            )

    # Sort by total quantity ascending
    low_performers.sort(key=lambda x: x[1])

    return low_performers


from datetime import datetime


def generate_sales_report(transactions, enriched_transactions, output_file="output/sales_report.txt"):
    """
    Generates a comprehensive formatted text report
    """

    # ---------- BASIC METRICS ----------
    total_transactions = len(transactions)
    total_revenue = sum(tx["quantity"] * tx["unit_price"] for tx in transactions)
    avg_order_value = total_revenue / total_transactions if total_transactions else 0

    dates = sorted(tx["date"] for tx in transactions)
    date_range = f"{dates[0]} to {dates[-1]}" if dates else "N/A"

    # ---------- REGION-WISE PERFORMANCE ----------
    region_stats = {}
    for tx in transactions:
        region = tx["region"]
        revenue = tx["quantity"] * tx["unit_price"]

        if region not in region_stats:
            region_stats[region] = {"sales": 0.0, "count": 0}

        region_stats[region]["sales"] += revenue
        region_stats[region]["count"] += 1

    region_stats = dict(
        sorted(region_stats.items(), key=lambda x: x[1]["sales"], reverse=True)
    )

    # ---------- TOP PRODUCTS ----------
    product_stats = {}
    for tx in transactions:
        name = tx["product_name"]
        if name not in product_stats:
            product_stats[name] = {"qty": 0, "revenue": 0.0}

        product_stats[name]["qty"] += tx["quantity"]
        product_stats[name]["revenue"] += tx["quantity"] * tx["unit_price"]

    top_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]["qty"],
        reverse=True
    )[:5]

    # ---------- TOP CUSTOMERS ----------
    customer_stats = {}
    for tx in transactions:
        cid = tx["customer_id"]
        revenue = tx["quantity"] * tx["unit_price"]

        if cid not in customer_stats:
            customer_stats[cid] = {"spent": 0.0, "orders": 0}

        customer_stats[cid]["spent"] += revenue
        customer_stats[cid]["orders"] += 1

    top_customers = sorted(
        customer_stats.items(),
        key=lambda x: x[1]["spent"],
        reverse=True
    )[:5]

    # ---------- DAILY SALES TREND ----------
    daily_stats = {}
    for tx in transactions:
        date = tx["date"]
        revenue = tx["quantity"] * tx["unit_price"]

        if date not in daily_stats:
            daily_stats[date] = {"revenue": 0.0, "count": 0, "customers": set()}

        daily_stats[date]["revenue"] += revenue
        daily_stats[date]["count"] += 1
        daily_stats[date]["customers"].add(tx["customer_id"])

    daily_stats = dict(sorted(daily_stats.items()))

    peak_day = max(
        daily_stats.items(),
        key=lambda x: x[1]["revenue"]
    )

    # ---------- LOW PERFORMING PRODUCTS ----------
    low_products = [
        (name, data["qty"], data["revenue"])
        for name, data in product_stats.items()
        if data["qty"] < 10
    ]

    # ---------- API ENRICHMENT SUMMARY ----------
    total_enriched = sum(1 for tx in enriched_transactions if tx.get("API_Match"))
    success_rate = (total_enriched / len(enriched_transactions)) * 100 if enriched_transactions else 0

    not_enriched_products = sorted({
        tx["product_name"]
        for tx in enriched_transactions
        if not tx.get("API_Match")
    })

    # ---------- WRITE REPORT ----------
    with open(output_file, "w", encoding="utf-8") as file:
        file.write("=" * 40 + "\n")
        file.write("SALES ANALYTICS REPORT\n")
        file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        file.write(f"Records Processed: {total_transactions}\n")
        file.write("=" * 40 + "\n\n")

        file.write("OVERALL SUMMARY\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Revenue: ₹{total_revenue:,.2f}\n")
        file.write(f"Total Transactions: {total_transactions}\n")
        file.write(f"Average Order Value: ₹{avg_order_value:,.2f}\n")
        file.write(f"Date Range: {date_range}\n\n")

        file.write("REGION-WISE PERFORMANCE\n")
        file.write("-" * 40 + "\n")
        for region, data in region_stats.items():
            percent = (data["sales"] / total_revenue) * 100
            file.write(
                f"{region:<10} ₹{data['sales']:,.2f}  "
                f"{percent:.2f}%  {data['count']} orders\n"
            )
        file.write("\n")

        file.write("TOP 5 PRODUCTS\n")
        file.write("-" * 40 + "\n")
        for i, (name, data) in enumerate(top_products, 1):
            file.write(
                f"{i}. {name} | Qty: {data['qty']} | Revenue: ₹{data['revenue']:,.2f}\n"
            )
        file.write("\n")

        file.write("TOP 5 CUSTOMERS\n")
        file.write("-" * 40 + "\n")
        for i, (cid, data) in enumerate(top_customers, 1):
            file.write(
                f"{i}. {cid} | Spent: ₹{data['spent']:,.2f} | Orders: {data['orders']}\n"
            )
        file.write("\n")

        file.write("DAILY SALES TREND\n")
        file.write("-" * 40 + "\n")
        for date, data in daily_stats.items():
            file.write(
                f"{date} | ₹{data['revenue']:,.2f} | "
                f"{data['count']} tx | {len(data['customers'])} customers\n"
            )
        file.write("\n")

        file.write("PRODUCT PERFORMANCE ANALYSIS\n")
        file.write("-" * 40 + "\n")
        file.write(f"Best Selling Day: {peak_day[0]} (₹{peak_day[1]['revenue']:,.2f})\n")

        if low_products:
            file.write("Low Performing Products:\n")
            for name, qty, rev in low_products:
                file.write(f"- {name}: Qty {qty}, Revenue ₹{rev:,.2f}\n")
        else:
            file.write("No low performing products found.\n")
        file.write("\n")

        file.write("API ENRICHMENT SUMMARY\n")
        file.write("-" * 40 + "\n")
        file.write(f"Total Products Enriched: {total_enriched}\n")
        file.write(f"Success Rate: {success_rate:.2f}%\n")
        file.write("Products Not Enriched:\n")
        for name in not_enriched_products:
            file.write(f"- {name}\n")

    print(f"Sales report generated at {output_file}")
