import tkinter as tk
from tkinter import messagebox
from collections import deque
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading

class Product:
    def __init__(self, name, quantity, cost, weight):
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.weight = weight
        self.related = []

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.lock = threading.Lock()

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, product, value):
        index = self.hash_function(product)
        with self.lock:
            for pair in self.table[index]:
                if pair[0] == product:
                    pair[1][0] = pair[1][0] + value[0]
                    pair[1][1] = pair[1][1] + value[1]
                    return
            self.table[index].append([product, value])

    def get_products(self, product):
        index = self.hash_function(product)
        with self.lock:
            for pair in self.table[index]:
                if pair[0] == product:
                    return pair[1]
            return None

class InventoryGraph:
    def __init__(self):
        self.graph = {}

    def add_product(self, product):
        if product.name not in self.graph:
            self.graph[product.name] = product

    def add_relationship(self, product1, product2):
        if product1.name in self.graph and product2.name in self.graph:
            self.graph[product1.name].related.append(product2.name)
            self.graph[product2.name].related.append(product1.name)

    def buy_product(self, pName, qty):
        totalWeight = 0
        price = 0
        products = []
        if pName in self.graph:
            availableQty = self.graph[pName].quantity
            if qty <= availableQty:
                availableQty = availableQty - qty
                self.graph[pName].quantity = availableQty
                totalWeight = totalWeight + (qty * self.graph[pName].weight)
                price = price + (qty * self.graph[pName].cost)
                products.append(totalWeight)
                products.append(price)
                print(products)
                print("Purchased successfully")
                print(availableQty)
                if availableQty < 5:
                    message = pName + " is out of stock"
                    msg = MIMEMultipart()
                    msg['From'] = senderEmail
                    msg['To'] = receiverEmail
                    msg['Subject'] = "Inventory Alert"
                    msg.attach(MIMEText(message, 'plain'))
                    server = smtplib.SMTP("smtp.gmail.com", 587)
                    server.starttls()
                    server.login(senderEmail, password)
                    server.sendmail(senderEmail, receiverEmail, msg.as_string())
                    server.quit()
            else:
                print("Out of stock")
        else:
            print("Product not found in inventory")
        return pName, products

    def update_product(self, pName, qty):
        if pName in self.graph:
            self.graph[pName].quantity = self.graph[pName].quantity + qty
            print("Updated Successfully")
        else:
            print("Product is not available")

    def display_inventory(self):
        for product, data in self.graph.items():
            print(f"Product: {product}, Quantity: {data.quantity}, Price: {data.cost}")
            if data.related:
                print("Related Products:")
                for related_product in data.related:
                    print(f"- {related_product}")
            print()

    def bfs(self, start_product):
        visited = set()
        queue = deque([start_product])

        while queue:
            current_product = queue.popleft()
            print(current_product.name)
            visited.add(current_product)
            for related_product_name in current_product.related:
                related_product = self.graph[related_product_name]
                if related_product not in visited:
                    queue.append(related_product)
                    visited.add(related_product)

def knapsack(Capacity):
    pNames = []
    weights = []
    profits = []
    for bucket in hash_table.table:
        for pair in bucket:
            pName = pair[0]
            weight, profit = pair[1][1][0], pair[1][1][1]
           
            if isinstance(weight, int) and isinstance(profit, int):
                pNames.append(pName)
                weights.append(weight)
                profits.append(profit)
            else:
                print(f"Invalid weight or profit for product {pName}")
    print(pNames, weights, profits)
    n = len(weights)
    return knapsack_util(Capacity, pNames, weights, profits, n)


def knapsack_util(Capacity, pNames, weight, profit, n):
    if n == 0 or Capacity == 0:
        return 0
    if int(weight[n - 1]) > Capacity:
        return knapsack_util(Capacity, pNames, weight, profit, n - 1)
    else:
        return max(profit[n - 1] + knapsack_util(Capacity - int(weight[n - 1]), pNames, weight, profit, n - 1),
                   knapsack_util(Capacity, pNames, weight, profit, n - 1))

def add_new_product():
    productName = newProductName.get()
    qty = int(newProductQty.get())
    price = int(newProductPrice.get())
    weight = int(newProductWeight.get())
    newProduct = Product(productName, qty, price, weight)
    inventory.add_product(newProduct)
    print("Product added")

def add_relationship():
    if product1Name.get() in inventory.graph and product2Name.get() in inventory.graph:
        inventory.graph[product1Name.get()].related.append(product2Name.get())
        inventory.graph[product2Name.get()].related.append(product1Name.get())
    display()

def sold_product_details():
    pName = soldProductName.get()
    messagebox.showinfo("Sold Product Details", f"{pName} Sold for {hash_table.get_products(pName)[1]}")

def display():
    inventory.display_inventory()

def buy():
    name = productName_buy.get()
    qty_str = quantity_buy.get()
    print(qty_str)
    if qty_str:
        qty = int(qty_str)
        products = inventory.buy_product(name, qty)
        hash_table.insert(name, products)
        print(hash_table.get_products(name))
    else:
        messagebox.showerror("Error", "Please enter a quantity.")

def update():
    name = productName_update.get()
    qty = int(quantity_update.get())
    inventory.update_product(name, qty)

def exit_app():
    window.destroy()

def show_add_product_page():
    clear_frame()
    add_product_frame.pack()

def show_buy_product_page():
    clear_frame()
    buy_product_frame.pack()

def show_update_product_page():
    clear_frame()
    update_product_frame.pack()

def show_display_inventory_page():
    clear_frame()
    display_inventory_frame.pack()

def show_knapsack_page():
    clear_frame()
    knapsack_frame.pack()

def knapsack_calculation():
    capacity_str = bag_capacity_entry.get()
    if capacity_str:
        capacity = int(capacity_str)
        profit = knapsack(capacity)
        messagebox.showinfo("Knapsack Profit", f"The maximum profit is: {profit}")
    else:
        messagebox.showerror("Error", "Please enter the bag capacity.")

def clear_frame():
    for frame in frames:
        frame.pack_forget()

senderEmail = "royalinventory03@gmail.com"
receiverEmail = "abhinivi67@gmail.com"
password = "hisr irsd jwif mutr"

inventory = InventoryGraph()
hash_table = HashTable(10)

# Adding products to inventory
product1 = Product("Laptop", 10, 65900, 20)
product2 = Product("Mouse", 20, 500, 10)
product3 = Product("Keyboard", 15, 1700, 15)

inventory.add_product(product1)
inventory.add_product(product2)
inventory.add_product(product3)

# Establishing relationships
inventory.add_relationship(product1, product2)
inventory.add_relationship(product1, product3)

# Initialize tkinter window
window = tk.Tk()
window.title("Inventory Management System")

# Frames
add_product_frame = tk.Frame(window)
buy_product_frame = tk.Frame(window)
update_product_frame = tk.Frame(window)
display_inventory_frame = tk.Frame(window)
knapsack_frame = tk.Frame(window)
frames = [add_product_frame, buy_product_frame, update_product_frame, display_inventory_frame, knapsack_frame]

# Labels and Entry Widgets for Add New Product
tk.Label(add_product_frame, text="New Product Name:").grid(row=0, column=0)
newProductName = tk.Entry(add_product_frame)
newProductName.grid(row=0, column=1)

tk.Label(add_product_frame, text="Quantity:").grid(row=1, column=0)
newProductQty = tk.Entry(add_product_frame)
newProductQty.grid(row=1, column=1)

tk.Label(add_product_frame, text="Price:").grid(row=2, column=0)
newProductPrice = tk.Entry(add_product_frame)
newProductPrice.grid(row=2, column=1)

tk.Label(add_product_frame, text="Weight:").grid(row=3, column=0)
newProductWeight = tk.Entry(add_product_frame)
newProductWeight.grid(row=3, column=1)

# Button for adding new product
tk.Button(add_product_frame, text="Add New Product", command=add_new_product).grid(row=4, column=0)

# Labels and Entry Widgets for Add Relationship
tk.Label(add_product_frame, text="Product 1:").grid(row=5, column=0)
product1Name = tk.Entry(add_product_frame)
product1Name.grid(row=5, column=1)

tk.Label(add_product_frame, text="Product 2:").grid(row=6, column=0)
product2Name = tk.Entry(add_product_frame)
product2Name.grid(row=6, column=1)

# Button for adding relationship
tk.Button(add_product_frame, text="Add Relationship", command=add_relationship).grid(row=7, column=0)

# Labels and Entry Widgets for Buy Product
tk.Label(buy_product_frame, text="Product Name:").grid(row=0, column=0)
productName_buy = tk.Entry(buy_product_frame)
productName_buy.grid(row=0, column=1)

tk.Label(buy_product_frame, text="Quantity:").grid(row=1, column=0)
quantity_buy = tk.Entry(buy_product_frame)
quantity_buy.grid(row=1, column=1)

# Button for buying product
tk.Button(buy_product_frame, text="Buy Product", command=buy).grid(row=2, column=0)
tk.Label(knapsack_frame, text="Bag Capacity:").grid(row=0, column=0)
bag_capacity_entry = tk.Entry(knapsack_frame)
bag_capacity_entry.grid(row=0, column=1)

# Button for calculating knapsack
tk.Button(knapsack_frame, text="Calculate Knapsack", command=knapsack_calculation).grid(row=1, column=0)
# Labels and Entry Widgets for Update Product
tk.Label(update_product_frame, text="Product Name:").grid(row=0, column=0)
productName_update = tk.Entry(update_product_frame)
productName_update.grid(row=0, column=1)

tk.Label(update_product_frame, text="Quantity:").grid(row=1, column=0)
quantity_update = tk.Entry(update_product_frame)
quantity_update.grid(row=1, column=1)

# Button for updating product
tk.Button(update_product_frame, text="Update Product", command=update).grid(row=2, column=0)

# Button for displaying inventory
tk.Button(display_inventory_frame, text="Display Inventory", command=display).grid(row=0, column=0)

# Button for displaying knapsack
tk.Button(display_inventory_frame, text="Knapsack", command=show_knapsack_page).grid(row=1, column=0)

# Labels and Entry Widgets for Sold Product Details
tk.Label(buy_product_frame, text="Product Name:").grid(row=3, column=0)
soldProductName = tk.Entry(buy_product_frame)
soldProductName.grid(row=3, column=1)

# Button for displaying sold product
tk.Button(buy_product_frame, text="Sold Product Details", command=sold_product_details).grid(row=4, column=0)

# Button to navigate to Add New Product page
tk.Button(window, text="Add New Product", command=show_add_product_page).pack()

# Button to navigate to Buy Product page
tk.Button(window, text="Buy Product", command=show_buy_product_page).pack()

# Button to navigate to Update Product page
tk.Button(window, text="Update Product", command=show_update_product_page).pack()

# Button to navigate to Display Inventory page
tk.Button(window, text="Display Inventory", command=show_display_inventory_page).pack()

# Button to navigate to Knapsack page
tk.Button(window, text="Knapsack", command=show_knapsack_page).pack()

# Button for exiting the application
tk.Button(window, text="Exit", command=exit_app).pack()

window.mainloop()

