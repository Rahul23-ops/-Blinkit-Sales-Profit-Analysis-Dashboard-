import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Generate a synthetic dataset mimicking Blinkit_Data.csv to make the charts render realistically
categories = [
    "Dairy & Bread", "Munchies", "Fruits & Vegetables", "Cold Drinks & Juices",
    "Bakery & Biscuits", "Instant & Frozen Food", "Tea, Coffee & Health Drinks",
    "Personal Care", "Cleaning Essentials", "Home & Office"
]

np.random.seed(42)
n_rows = 500
data = {
    "Category": np.random.choice(categories, n_rows),
    "Total_Price": np.random.uniform(50, 500, n_rows),
}
# Profit is somewhat correlated with Total_Price but has variance
data["Profit"] = data["Total_Price"] * np.random.uniform(0.1, 0.35, n_rows) - np.random.uniform(0, 10, n_rows)

df = pd.DataFrame(data)

# Ensure output directory exists
os.makedirs("blinkit_charts", exist_ok=True)

# Style parameters for clean professional look
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10
accent_color = '#10b981' # Emerald green suitable for grocery/Blinkit theme
secondary_color = '#3b82f6'

# 1. Sales by Category
sales_by_category = df.groupby("Category")["Total_Price"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
sales_by_category.plot(kind="bar", color=accent_color, edgecolor='#047857', linewidth=0.7)
plt.title("Sales by Category", fontsize=14, fontweight='bold', pad=15, color='#1f2937')
plt.xlabel("Category", fontsize=11, labelpad=10, color='#4b5563')
plt.ylabel("Total Sales ($)", fontsize=11, labelpad=10, color='#4b5563')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("blinkit_charts/sales_by_category.png", dpi=200)
plt.close()

# 2. Profit by Category
profit_by_category = df.groupby("Category")["Profit"].sum().sort_values(ascending=False)
plt.figure(figsize=(9, 5))
profit_by_category.plot(kind="bar", color=secondary_color, edgecolor='#1d4ed8', linewidth=0.7)
plt.title("Profit by Category", fontsize=14, fontweight='bold', pad=15, color='#1f2937')
plt.xlabel("Category", fontsize=11, labelpad=10, color='#4b5563')
plt.ylabel("Total Profit ($)", fontsize=11, labelpad=10, color='#4b5563')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("blinkit_charts/profit_by_category.png", dpi=200)
plt.close()

# 3. Profit Distribution
plt.figure(figsize=(7, 7))
colors = ['#10b981', '#3b82f6', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899', '#14b8a6', '#f97316', '#6b7280', '#a855f7']
profit_by_category.plot(kind="pie", autopct="%1.1f%%", colors=colors, wedgeprops={'edgecolor': 'white', 'linewidth': 1})
plt.title("Profit Distribution by Category", fontsize=14, fontweight='bold', pad=15, color='#1f2937')
plt.ylabel("")
plt.tight_layout()
plt.savefig("blinkit_charts/profit_distribution.png", dpi=200)
plt.close()

# 4. Sales vs Profit
summary = df.groupby("Category").agg({
    "Total_Price":"sum",
    "Profit":"sum"
}).reset_index()

plt.figure(figsize=(9, 5.5))
plt.scatter(summary["Total_Price"], summary["Profit"], color='#ec4899', s=100, alpha=0.8, edgecolor='#be185d', zorder=3)

for i in range(len(summary)):
    plt.text(
        summary["Total_Price"][i] + 150,
        summary["Profit"][i] - 10,
        summary["Category"][i],
        fontsize=9,
        color='#374151',
        weight='medium'
    )

plt.title("Sales vs Profit by Category", fontsize=14, fontweight='bold', pad=15, color='#1f2937')
plt.xlabel("Total Sales ($)", fontsize=11, labelpad=10, color='#4b5563')
plt.ylabel("Total Profit ($)", fontsize=11, labelpad=10, color='#4b5563')
plt.grid(linestyle='--', alpha=0.5, zorder=1)
# Add some margin to text doesn't clip
plt.xlim(summary["Total_Price"].min() - 1000, summary["Total_Price"].max() + 3500)
plt.tight_layout()
plt.savefig("blinkit_charts/sales_vs_profit.png", dpi=200)
plt.close()

print("Charts successfully generated.")