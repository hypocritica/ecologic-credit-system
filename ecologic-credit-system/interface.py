import tkinter as tk
from tkinter import messagebox
import requests
import json
import socket

global hostip
hostip = 'http://138.195.53.65:5000'

def get_local_address():
    # Get the local IP address of the machine
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip


def mine_block():
    try:
        response = requests.get(hostip + '/mine')
        if response.status_code == 200:
            messagebox.showinfo("Mine Block", "Block mined successfully!\n" + json.dumps(response.json(), indent=4))
        else:
            messagebox.showerror("Mine Block", "Failed to mine block.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def calculate_amount():
    # Calculate amount based on selected options
    selected_options = [var.get() for var in option_vars if var.get() != "None"]
    amount = sum(option_values[option] for option in selected_options)
    amount_entry.delete(0, tk.END)
    amount_entry.insert(0, str(amount))


def new_transaction():
    try:
        sender = get_local_address()
        recipient = recipient_entry.get()
        amount = amount_entry.get()
        data = {
            "sender": sender,
            "recipient": recipient,
            "amount": int(amount)
        }
        response = requests.post(hostip + '/new', json=data)
        if response.status_code == 201:
            messagebox.showinfo("New Transaction", response.json()["message"])
        else:
            messagebox.showerror("New Transaction", "Failed to create transaction.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def view_chain():
    try:
        response = requests.get(hostip + '/chain')
        if response.status_code == 200:
            chain_data = json.dumps(response.json(), indent=4)
            messagebox.showinfo("Blockchain", chain_data)
        else:
            messagebox.showerror("View Chain", "Failed to retrieve blockchain.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


# Setup Tkinter window
root = tk.Tk()
root.title("Blockchain User Interface")

# Mine Block Button
mine_button = tk.Button(root, text="Mine Block", command=mine_block)
mine_button.pack(pady=10)

# New Transaction Section
tk.Label(root, text="New Transaction:").pack(pady=5)
tk.Label(root, text="Sender Address:").pack()
sender_entry = tk.Entry(root)
sender_entry.insert(0, get_local_address())
sender_entry.config(state='disabled')
sender_entry.pack()
tk.Label(root, text="Recipient Address (Default: address2):").pack()
recipient_entry = tk.Entry(root)
recipient_entry.insert(0, "address2")
recipient_entry.pack()

# Amount Calculation Section
tk.Label(root, text="Options for Amount Calculation:").pack(pady=5)
option_values = {"Option A": 1, "Option B": 1.5, "Option C": 2}
option_vars = []
for option, value in option_values.items():
    var = tk.StringVar(value="None")
    option_vars.append(var)
    tk.Checkbutton(root, text=f"{option} ({value})", variable=var, onvalue=option, offvalue="None", command=calculate_amount).pack()

tk.Label(root, text="Amount:").pack()
amount_entry = tk.Entry(root)
amount_entry.pack()

# Create Transaction Button
transaction_button = tk.Button(root, text="Create Transaction", command=new_transaction)
transaction_button.pack(pady=10)

# View Blockchain Button
view_chain_button = tk.Button(root, text="View Full Blockchain", command=view_chain)
view_chain_button.pack(pady=10)

# Start Tkinter loop
root.mainloop()
