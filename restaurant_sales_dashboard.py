"""
Restaurant Sales Dashboard  (PS No. 77)
Language : Python 3
Concepts : Pandas, Matplotlib, CSV, GroupBy

Usage:  python restaurant_sales_dashboard.py [csv_file]
        (default file: restaurant_sales.csv)
"""
import sys
import pandas as pd
import matplotlib.pyplot as plt


def load_data(filename):
    """Read CSV, skip invalid rows with a warning, add Sales = Quantity x Price."""
    try:
        df = pd.read_csv(filename, dtype=str)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    except pd.errors.EmptyDataError:
        print(f"Error: File '{filename}' is empty.")
        return None

    needed = ["Date", "Item", "Category", "Quantity", "Price"]
    if not all(col in df.columns for col in needed):
        print("Error: CSV must have columns: " + ", ".join(needed))
        return None

    qty = pd.to_numeric(df["Quantity"], errors="coerce")   # text -> NaN
    price = pd.to_numeric(df["Price"], errors="coerce")

    keep = []
    for i in range(len(df)):
        row_no = i + 2   # file line number (line 1 is the header)
        if pd.isna(qty[i]):
            print(f"Warning: Row {row_no} skipped - Quantity must be a number.")
            keep.append(False)
        elif pd.isna(price[i]):
            print(f"Warning: Row {row_no} skipped - Price must be a number.")
            keep.append(False)
        elif qty[i] < 0 or price[i] < 0:
            print(f"Warning: Row {row_no} skipped - Quantity and Price must be 0 or more.")
            keep.append(False)
        elif pd.isna(df.loc[i, "Item"]) or pd.isna(df.loc[i, "Category"]) or pd.isna(df.loc[i, "Date"]):
            print(f"Warning: Row {row_no} skipped - Date, Item and Category are required.")
            keep.append(False)
        else:
            keep.append(True)

    df = df[keep].copy()
    df["Quantity"] = qty[keep]
    df["Price"] = price[keep]
    df["Sales"] = df["Quantity"] * df["Price"]      # Sales = Quantity x Price
    return df


def sales_by_category(df):
    cat = df.groupby("Category")["Sales"].sum().sort_values(ascending=False)
    for name, amount in cat.items():
        print(f"{name} : Rs. {amount:.0f}")
    print(f"Total sales: Rs. {cat.sum():.0f}")

    plt.figure(figsize=(6, 4))
    plt.bar(cat.index, cat.values, color="seagreen")
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales (Rs.)")
    plt.tight_layout()
    plt.savefig("sales_by_category.png")
    plt.show()


def top_items(df, show_total=True):
    by_qty = df.groupby("Item")["Quantity"].sum()
    by_rev = df.groupby("Item")["Sales"].sum()

    if show_total:
        print(f"Total sales: Rs. {df['Sales'].sum():.0f}")
    q_item, q_val = by_qty.idxmax(), by_qty.max()
    unit = "unit" if q_val == 1 else "units"
    print(f"Top item by quantity: {q_item} ({q_val:.0f} {unit})")
    print(f"Top item by revenue: {by_rev.idxmax()} (Rs. {by_rev.max():.0f})")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    by_qty.sort_values().plot(kind="barh", ax=axes[0], color="orange", title="Quantity Sold by Item")
    by_rev.sort_values().plot(kind="barh", ax=axes[1], color="steelblue", title="Revenue by Item (Rs.)")
    plt.tight_layout()
    plt.savefig("top_items.png")
    plt.show()


def daily_sales(df):
    daily = df.groupby("Date")["Sales"].sum()
    for date, amount in daily.items():
        print(f"{date} : Rs. {amount:.0f}")
    print(f"Best day: {daily.idxmax()}")

    plt.figure(figsize=(6, 4))
    plt.plot(daily.index, daily.values, marker="o", color="crimson")
    plt.title("Daily Sales")
    plt.xlabel("Date")
    plt.ylabel("Sales (Rs.)")
    plt.tight_layout()
    plt.savefig("daily_sales.png")
    plt.show()


def main():
    filename = sys.argv[1] if len(sys.argv) > 1 else "restaurant_sales.csv"
    df = load_data(filename)
    if df is None:
        return
    if df.empty:
        print("No valid data to analyse.")
        return

    while True:
        print("\n===== Restaurant Sales Dashboard =====")
        print("1. Sales by category")
        print("2. Top items")
        print("3. Daily sales")
        print("4. Top items and daily sales")
        print("5. Exit")
        choice = input("Enter choice: ").strip()
        if choice == "1":
            sales_by_category(df)
        elif choice == "2":
            top_items(df)
        elif choice == "3":
            daily_sales(df)
        elif choice == "4":
            top_items(df, show_total=False)
            daily_sales(df)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1 to 5.")


if __name__ == "__main__":
    main()
