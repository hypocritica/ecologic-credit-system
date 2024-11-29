import tkinter as tk
from tkinter import messagebox
import requests
import json
import socket
import re
import utils
from ecdsa import SigningKey
from transaction import Transaction

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


def new_transaction():
    try:
        sender = get_local_address()
        destinataire = destinataire_entry.get()
        message = message_entry.get()
        value = value_entry.get()
        
        # Validate the value for compulsory +/- sign
        val_pattern = r"^[-+][0-9]+$"
        if not re.match(val_pattern, value):
            messagebox.showerror("Input Error", "Value must start with '+' for credits gained or '-' for credits lost.")
            return
        
        sk = SigningKey.generate()

        t = Transaction(message, value, destinataire)
        t.sign(sk)

        # Transaction data
        data = {
            "message": t.message,
            "value": t.value,
            "dest": t.dest,
            "date": t.date,
            "author": t.author,
            "vk": t.vk,
            "signature": t.signature 
        }

        # Send transaction to the backend
        response = requests.post(hostip + '/transactions/new', json=data)
        if response.status_code == 201:
            messagebox.showinfo("New Transaction", response.json()["message"])
        else:
            messagebox.showerror("New Transaction", "Failed to create transaction.")
    except ValueError:
        messagebox.showerror("Input Error", "Value must be a valid integer starting with '+' or '-'.")
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
root.title("Ecological Credit System")

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

# New Destinataire Field
tk.Label(root, text="Destinataire (Hash):").pack()
destinataire_entry = tk.Entry(root)
destinataire_entry.pack()

# New Section for Message and Value
tk.Label(root, text="Message for Transaction:").pack(pady=5)
message_entry = tk.Entry(root)
message_entry.pack()

tk.Label(root, text="Value of Credits Lost/Gained (e.g., +10 or -10):").pack(pady=5)
value_entry = tk.Entry(root)
value_entry.pack()

# Create Transaction Button
transaction_button = tk.Button(root, text="Create Transaction", command=new_transaction)
transaction_button.pack(pady=10)

# View Blockchain Button
view_chain_button = tk.Button(root, text="View Full Blockchain", command=view_chain)
view_chain_button.pack(pady=10)

# Start Tkinter loop
root.mainloop()
