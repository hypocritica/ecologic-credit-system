import tkinter as tk
from tkinter import messagebox
import requests
import json

# Replace SERVER_IP with the actual IP address of the server running the Flask application
server_ip = '138.195.57.189'  # Example server IP address

# Define the Flask server URL
base_url = f'http://{server_ip}:5000'

def get_full_chain():
    try:
        response = requests.get(f'{base_url}/chain')
        if response.status_code == 200:
            chain_data = json.dumps(response.json(), indent=4)
            messagebox.showinfo("Blockchain", chain_data)
        else:
            messagebox.showerror("Error", "Failed to retrieve blockchain.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def add_transaction():
    try:
        message = message_entry.get()
        author = author_entry.get()
        vk = vk_entry.get()
        signature = signature_entry.get()
        value = value_entry.get()
        dest = dest_entry.get()
        date = date_entry.get()

        data = {
            "message": message,
            "author": author,
            "vk": vk,
            "signature": signature,
            "value": value,
            "dest": dest,
            "date": date
        }
        response = requests.post(f'{base_url}/transactions/new', json=data)
        if response.status_code == 201:
            messagebox.showinfo("New Transaction", response.json()["message"])
        else:
            messagebox.showerror("Error", "Failed to add transaction.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def mine_block():
    try:
        response = requests.get(f'{base_url}/mine')
        if response.status_code == 200:
            mine_data = json.dumps(response.json(), indent=4)
            messagebox.showinfo("Mine Block", mine_data)
        else:
            messagebox.showerror("Error", "Failed to mine block.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def validate_chain():
    try:
        response = requests.get(f'{base_url}/chain/validate')
        if response.status_code == 200:
            validation_data = response.json()
            messagebox.showinfo("Validate Chain", validation_data['message'])
        else:
            messagebox.showerror("Error", "Failed to validate chain.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def merge_chain():
    try:
        response = requests.get(f'{base_url}/chain')
        if response.status_code == 200:
            chain_data = response.json()
            merge_response = requests.post(f'{base_url}/chain/merge', json={'chain': chain_data['chain']})
            if merge_response.status_code == 200:
                messagebox.showinfo("Merge Chain", merge_response.json()["message"])
            else:
                messagebox.showerror("Error", "Failed to merge chain.")
        else:
            messagebox.showerror("Error", "Failed to retrieve chain for merging.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Setup Tkinter window
root = tk.Tk()
root.title("Blockchain User Interface")

# View Full Blockchain Button
view_chain_button = tk.Button(root, text="View Full Blockchain", command=get_full_chain)
view_chain_button.pack(pady=5)

# New Transaction Section
tk.Label(root, text="New Transaction:").pack(pady=5)
message_label = tk.Label(root, text="Message:")
message_label.pack()
message_entry = tk.Entry(root)
message_entry.pack()

author_label = tk.Label(root, text="Author:")
author_label.pack()
author_entry = tk.Entry(root)
author_entry.pack()

vk_label = tk.Label(root, text="Verification Key (VK):")
vk_label.pack()
vk_entry = tk.Entry(root)
vk_entry.pack()

signature_label = tk.Label(root, text="Signature:")
signature_label.pack()
signature_entry = tk.Entry(root)
signature_entry.pack()

value_label = tk.Label(root, text="Value:")
value_label.pack()
value_entry = tk.Entry(root)
value_entry.pack()

dest_label = tk.Label(root, text="Destination Address:")
dest_label.pack()
dest_entry = tk.Entry(root)
dest_entry.pack()

date_label = tk.Label(root, text="Date:")
date_label.pack()
date_entry = tk.Entry(root)
date_entry.pack()

transaction_button = tk.Button(root, text="Create Transaction", command=add_transaction)
transaction_button.pack(pady=10)

# Mine Block Button
mine_button = tk.Button(root, text="Mine Block", command=mine_block)
mine_button.pack(pady=5)

# Validate Blockchain Button
validate_button = tk.Button(root, text="Validate Blockchain", command=validate_chain)
validate_button.pack(pady=5)

# Merge Blockchain Button
merge_button = tk.Button(root, text="Merge Blockchain", command=merge_chain)
merge_button.pack(pady=5)

# Start Tkinter loop
root.mainloop()
