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
