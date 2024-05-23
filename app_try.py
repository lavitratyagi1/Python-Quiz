import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Login Page")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        self.username_label = tk.Label(root, text="Username", bg="#f0f0f0")
        self.username_label.pack(pady=10)
        self.username_entry = tk.Entry(root)
        self.username_entry.pack(pady=5)
        
        self.submit_button = tk.Button(root, text="Submit", command=self.check_username, bg="#4CAF50", fg="white")
        self.submit_button.pack(pady=5)
        
        self.password_label = tk.Label(root, text="Password", bg="#f0f0f0")
        self.password_entry = tk.Entry(root, show="*")
        self.login_button = tk.Button(root, text="Login", command=self.check_password, bg="#4CAF50", fg="white")
        self.create_button = tk.Button(root, text="Create Account", command=self.create_account, bg="#4CAF50", fg="white")
        
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="lavitra",
            password="1234567890",
            database="oops_project"
        )
        self.db_cursor = self.db_connection.cursor()

    def check_username(self):
        username = self.username_entry.get()
        query = "SELECT * FROM users WHERE username = %s"
        self.db_cursor.execute(query, (username,))
        result = self.db_cursor.fetchone()
        
        if result:
            self.password_label.pack(pady=5)
            self.password_entry.pack(pady=5)
            self.login_button.pack(pady=5)
        else:
            self.password_label.pack(pady=5)
            self.password_entry.pack(pady=5)
            self.create_button.pack(pady=5)

    def check_password(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        self.db_cursor.execute(query, (username, password))
        result = self.db_cursor.fetchone()
        
        if result:
            messagebox.showinfo("Login Successful", "Welcome!")
            self.open_homepage(username)
        else:
            messagebox.showerror("Error", "Incorrect password")

    def create_account(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        self.db_cursor.execute(query, (username, password))
        self.db_connection.commit()
        messagebox.showinfo("Account Created", "Your account has been created successfully!")
        self.password_label.pack_forget()
        self.password_entry.pack_forget()
        self.create_button.pack_forget()
        self.login_button.pack_forget()

    def open_homepage(self, username):
        self.root.destroy()  # Close the login window
        python_executable = sys.executable
        subprocess.call([python_executable, "homepage.py", username])  # Open the homepage interface with username

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()

    # Close the database connection when done
    app.db_cursor.close()
    app.db_connection.close()
