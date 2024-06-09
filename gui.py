import tkinter as tk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import csv

# Function to connect to MySQL database
def connect_to_database():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            database='inventory_db',
            user='root',
            password='GoodLuck123!'
        )
        if conn.is_connected():
            messagebox.showinfo("Success", "Connected to MySQL database successfully.")
            return conn
    except Error as e:
        messagebox.showerror("Error", f"Error connecting to MySQL database: {e}")
        return None

# Function to add a new inventory entry to MySQL database
def add_inventory_to_database(conn, item_name, item_qty):
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (item_name, item_qty) VALUES (%s, %s)", (item_name, item_qty))
        conn.commit()
        messagebox.showinfo("Success", f"{item_name} added to inventory.")
        cursor.close()
    except Error as e:
        messagebox.showerror("Error", f"Error adding item to inventory: {e}")

# Function to add a new inventory entry to CSV file
def add_inventory_to_csv(item_name, item_qty):
    with open('inventory.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([item_name, item_qty])

# Function to add a new inventory entry
def add_inventory():
    item_name = item_name_entry.get()
    item_qty = item_qty_entry.get()

    if not item_name or not item_qty:
        messagebox.showerror("Error", "Please enter both item name and quantity.")
        return

    try:
        item_qty = int(item_qty)
        if item_qty < 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Error", "Quantity must be a positive integer.")
        return

    if database_enabled.get():
        conn = connect_to_database()
        if conn:
            add_inventory_to_database(conn, item_name, item_qty)
    else:
        add_inventory_to_csv(item_name, item_qty)

    item_name_entry.delete(0, tk.END)
    item_qty_entry.delete(0, tk.END)

# Function to generate a full list of inventory from MySQL database
def generate_inventory_from_database(conn=None):
    try:
        if conn is None:
            conn = connect_to_database() 
            if conn is None: 
                return

        cursor = conn.cursor()
        cursor.execute("SELECT item_name, item_qty FROM inventory") 
        rows = cursor.fetchall()
        if rows:
            inventory_text = '\n'.join([f'{name} - {qty}' for name, qty in rows])
            result_label.config(text=inventory_text)
        else:
            result_label.config(text="No items found in inventory.")
        cursor.close()
    except Error as e:
        messagebox.showerror("Error", f"Error fetching inventory from database: {e}")


# Function to generate a full list of inventory
def generate_inventory(conn=None):
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT item_name, item_qty FROM inventory") 
            rows = cursor.fetchall()
            if rows:
                inventory_text = '\n'.join([f'{name} - {qty}' for name, qty in rows])
                result_label.config(text=inventory_text)
            else:
                result_label.config(text="No items found in inventory.")
            cursor.close()
        except Error as e:
            messagebox.showerror("Error", f"Error fetching inventory from database: {e}")
    else:
        generate_inventory_from_database()
# Function to remove an item from MySQL database
def remove_inventory_from_database(conn, item_name):
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE item_name = %s", (item_name,))
        conn.commit()
        messagebox.showinfo("Success", f"{item_name} removed from inventory.")
        cursor.close()
    except Error as e:
        messagebox.showerror("Error", f"Error removing item from inventory: {e}")

# Function to remove an item from the database
def remove_inventory(item_name):
    if database_enabled.get():  # Check if database mode is enabled
        conn = connect_to_database()
        if conn:
            remove_inventory_from_database(conn, item_name)
    else:
        messagebox.showerror("Error", "Database mode is not enabled.")

# Function to authenticate user
def authenticate_user():
    username = username_entry.get()
    password = password_entry.get()

    # Dummy authentication, replace with your actual authentication logic
    if username == 'admin' and password == 'password':
        messagebox.showinfo("Success", "Authentication successful.")
        login_frame.pack_forget()
        main_frame.pack()
    else:
        messagebox.showerror("Error", "Invalid username or password.")

# create the main window
root = tk.Tk()
root.title("Inventory Management")

# Frame for login
login_frame = tk.Frame(root)
login_frame.pack()

# input fields for login
username_label = tk.Label(login_frame, text="Username:")
username_label.grid(row=0, column=0, padx=5, pady=5)
username_entry = tk.Entry(login_frame)
username_entry.grid(row=0, column=1, padx=5, pady=5)
password_label = tk.Label(login_frame, text="Password:")
password_label.grid(row=1, column=0, padx=5, pady=5)
password_entry = tk.Entry(login_frame, show="*")
password_entry.grid(row=1, column=1, padx=5, pady=5)
login_button = tk.Button(login_frame, text="Login", command=authenticate_user)
login_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# Frame for main inventory management
main_frame = tk.Frame(root)

# input fields for inventory management
item_name_label = tk.Label(main_frame, text="Item Name:")
item_name_label.grid(row=0, column=0, padx=5, pady=5)
item_name_entry = tk.Entry(main_frame)
item_name_entry.grid(row=0, column=1, padx=5, pady=5)
item_qty_label = tk.Label(main_frame, text="Item Quantity:")
item_qty_label.grid(row=1, column=0, padx=5, pady=5)
item_qty_entry = tk.Entry(main_frame)
item_qty_entry.grid(row=1, column=1, padx=5, pady=5)

# checkbox for enabling database
database_enabled = tk.BooleanVar()
database_checkbox = tk.Checkbutton(main_frame, text="Use MySQL Database", variable=database_enabled)
database_checkbox.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

# creating the buttons for inventory management
add_button = tk.Button(main_frame, text="Add Inventory", command=add_inventory)
add_button.grid(row=3, column=0, padx=5, pady=5)
remove_button = tk.Button(main_frame, text="Remove Inventory", command=lambda: remove_inventory(remove_item_entry.get()))
remove_button.grid(row=3, column=1, padx=5, pady=5)
generate_button = tk.Button(main_frame, text="Generate Inventory", command=generate_inventory)
generate_button.grid(row=4, column=0, padx=5, pady=5)

# input field for removing an item
remove_item_label = tk.Label(main_frame, text="Item Name to Remove:")
remove_item_label.grid(row=4, column=1, padx=5, pady=5)
remove_item_entry = tk.Entry(main_frame)
remove_item_entry.grid(row=4, column=2, padx=5, pady=5)

# label for displaying inventory
result_label = tk.Label(main_frame, text="List")
result_label.grid(row=5, column=0, columnspan=3, padx=5, pady=5)

main_frame.pack()


root.mainloop()
