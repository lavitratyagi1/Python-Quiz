import tkinter as tk
from tkinter import ttk
import mysql.connector

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
            user="root",
            password="123456",
            database="login"
        )
        self.db_cursor = self.db_connection.cursor()

        self.load_leaderboard()

    def load_leaderboard(self):
        query = "SELECT username, score FROM score ORDER BY score DESC, username ASC"
        self.db_cursor.execute(query)
        results = self.db_cursor.fetchall()

        for idx, (username, score) in enumerate(results, start=1):
            self.tree.insert("", "end", values=(idx, username, score))

if __name__ == "__main__":
    root = tk.Tk()
    app = LeaderboardApp(root)
    root.mainloop()