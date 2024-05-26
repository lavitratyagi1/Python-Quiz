import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class DashboardApp:
    def __init__(self, root, username, leaderboard_app):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        self.username = username  # Store the username for future reference

        self.name_label = tk.Label(root, text="Name:", bg="#f0f0f0")
        self.name_label.pack(pady=10)
        self.name_value = tk.Label(root, text="", bg="#f0f0f0")
        self.name_value.pack(pady=5)

        self.score_label = tk.Label(root, text="Score:", bg="#f0f0f0")
        self.score_label.pack(pady=10)
        self.score_value = tk.Label(root, text="", bg="#f0f0f0")
        self.score_value.pack(pady=5)

        self.rank_label = tk.Label(root, text="Rank:", bg="#f0f0f0")
        self.rank_label.pack(pady=10)
        self.rank_value = tk.Label(root, text="", bg="#f0f0f0")
        self.rank_value.pack(pady=5)

        self.leaderboard_button = tk.Button(root, text="Go to Leaderboard", command=self.open_leaderboard, bg="#4CAF50", fg="white")
        self.leaderboard_button.pack(pady=20)

        self.account_button = tk.Button(root, text="View Account", command=self.open_account, bg="#4CAF50", fg="white")
        self.account_button.pack(pady=20)

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="lavitra",
            password="1234567890",
            database="oops_project"
        )
        self.db_cursor = self.db_connection.cursor()

        self.leaderboard_app = leaderboard_app
        self.load_user_data(username)

    def load_user_data(self, username):
        query = "SELECT username, score FROM scores WHERE username = %s"
        self.db_cursor.execute(query, (username,))
        result = self.db_cursor.fetchone()

        if result:
            username, score = result
            self.name_value.config(text=username)
            self.score_value.config(text=score)

            # Get rank from LeaderboardApp's rank_dict if leaderboard_app is not None
            if self.leaderboard_app:
                rank = self.leaderboard_app.rank_dict.get(username, "N/A")
            else:
                rank = "N/A"
            self.rank_value.config(text=rank)
        else:
            messagebox.showerror("Error", "User data not found")

    def open_leaderboard(self):
        self.root.destroy()
        root = tk.Tk()
        app = LeaderboardApp(root)
        root.mainloop()

    def open_account(self):
        self.root.destroy()
        root = tk.Tk()
        app = AccountApp(root, self.username)
        root.mainloop()


class LeaderboardApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Leaderboard")
        self.root.geometry("400x300")
        self.root.configure(bg="#2c3e50")

        # Style configuration
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview",
                        background="#34495e",
                        foreground="white",
                        rowheight=25,
                        fieldbackground="#34495e")
        style.map('Treeview', background=[('selected', '#2980b9')])

        style.configure("Treeview.Heading",
                        background="#1abc9c",
                        foreground="white",
                        font=("Arial", 12, "bold"))

        # Treeview widget
        self.tree = ttk.Treeview(root, columns=("Rank", "Username", "Score"), show="headings")
        self.tree.heading("Rank", text="Rank")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Score", text="Score")
        self.tree.column("Rank", anchor=tk.CENTER, width=50)
        self.tree.column("Username", anchor=tk.CENTER, width=150)
        self.tree.column("Score", anchor=tk.CENTER, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Scrollbar
        scrollbar = ttk.Scrollbar(root, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Database connection
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="lavitra",
            password="1234567890",
            database="oops_project"
        )
        self.db_cursor = self.db_connection.cursor()

        self.rank_dict = {}
        self.load_leaderboard()

    def load_leaderboard(self):
        query = "SELECT username, score FROM scores ORDER BY score DESC, username ASC"
        self.db_cursor.execute(query)
        results = self.db_cursor.fetchall()

        for idx, (username, score) in enumerate(results, start=1):
            self.tree.insert("", "end", values=(idx, username, score))
            self.rank_dict[username] = idx


class AccountApp:
    def __init__(self, root, username):
        self.root = root
        self.root.title("Account Page")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")
        
        self.username = username

        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="lavitra",
            password="1234567890",
            database="oops_project"
        )
        self.db_cursor = self.db_connection.cursor()

        self.load_account_data()

    def load_account_data(self):
        query = "SELECT username, password FROM users WHERE username = %s"
        self.db_cursor.execute(query, (self.username,))
        result = self.db_cursor.fetchone()
        
        if result:
            username, password = result

            self.username_label = tk.Label(self.root, text=f"Username: {username}", bg="#f0f0f0")
            self.username_label.pack(pady=10)
            
            self.password_label = tk.Label(self.root, text=f"Password: {password}", bg="#f0f0f0")
            self.password_label.pack(pady=10)
        else:
            messagebox.showerror("Error", "User data not found")


if __name__ == "__main__":
    root = tk.Tk()
    username = "lapi"  # Replace with actual username as needed
    leaderboard_app = LeaderboardApp(tk.Tk())
    root.destroy()  # Destroy the temporary leaderboard window
    root = tk.Tk()
    app = DashboardApp(root, username, leaderboard_app)
    root.mainloop()
