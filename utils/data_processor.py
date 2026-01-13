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
