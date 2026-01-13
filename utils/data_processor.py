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
