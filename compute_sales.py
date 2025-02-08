"""
Martin Acevedo
A01794756

This script computes total sales from a sales record JSON file
using product prices from a price catalogue JSON file.
Results are output to both console and file.
"""

import json
import sys
import time


def load_json(file_path):
    """Load JSON data from a file and handle errors."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in file - {file_path}")
    return None


def parse_price_catalogue(price_catalogue):
    """Convert price catalogue list into a dictionary."""
    price_dict = {}
    for item in price_catalogue:
        if "title" in item and "price" in item:
            if not isinstance(item["price"], (int, float)):
                print(f"Warning: {item['title']} has an invalid price")
                price_dict[item["title"]] = 0.0
            else:
                price_dict[item["title"]] = item["price"]
        else:
            print(f"Warning: Invalid product entry {item}")
    return price_dict


def parse_sales_record(sales_record):
    """Convert sales record list to a standard format."""
    parsed_sales = []
    for sale in sales_record:
        if "Product" in sale and "Quantity" in sale:
            if not isinstance(sale["Quantity"], (int, float)):
                print(f"Warning: Invalid quantity for {sale['Product']}")
                sale["Quantity"] = 0
            parsed_sales.append({
                "product": sale["Product"],
                "quantity": sale["Quantity"]
            })
        else:
            print(f"Warning: Invalid sales entry {sale}")
    return parsed_sales


def compute_total_sales(price_catalogue, sales_record):
    """Compute the total sales amount."""
    total_cost = 0.0
    errors = []

    for sale in sales_record:
        product = sale.get("product")
        quantity = sale.get("quantity")

        if product not in price_catalogue:
            errors.append(f"Error: Product '{product}' not in catalogue.")
            continue

        if not isinstance(quantity, (int, float)):
            errors.append(f"Error: Invalid qty '{quantity}' for '{product}'.")
            continue

        total_cost += price_catalogue[product] * quantity

    return total_cost, errors


def main():
    """Main function to process sales and generate a report."""
    if len(sys.argv) != 3:
        print("Usage: python compute_sales.py price_name.json sales_name.json")
        sys.exit(1)

    price_catalogue_file, sales_record_file = sys.argv[1], sys.argv[2]
    start_time = time.time()

    price_catalogue_data = load_json(price_catalogue_file)
    sales_record_data = load_json(sales_record_file)

    if price_catalogue_data is None or sales_record_data is None:
        print("Exiting due to file loading errors.")
        sys.exit(1)

    price_catalogue = parse_price_catalogue(price_catalogue_data)
    sales_record = parse_sales_record(sales_record_data)
    total_sales, errors = compute_total_sales(price_catalogue, sales_record)

    elapsed_time = time.time() - start_time

    output = [
        "Sales Report",
        "=" * 30,
        f"Total Sales Amount: ${total_sales:.2f}",
        f"Execution Time: {elapsed_time:.4f} sec",
        "\nErrors:",
    ]
    output.extend(errors if errors else ["No errors encountered."])

    result_text = "\n".join(output)

    print(result_text)

    with open("SalesResults.txt", "w", encoding="utf-8") as result_file:
        result_file.write(result_text)


if __name__ == "__main__":
    main()
