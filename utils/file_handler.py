def read_sales_data(filename):
    """
    Reads sales data from file handling encoding issues

    Returns: list of raw lines (strings)
    """

    encodings_to_try = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings_to_try:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                all_lines = file.readlines()
                break
        except UnicodeDecodeError:
            continue
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return []

    else:
        print("Error: Unable to read file due to encoding issues.")
        return []

    # Skip header and clean empty lines
    for line in all_lines[1:]:
        line = line.strip()
        if line:
            lines.append(line)

    return lines
