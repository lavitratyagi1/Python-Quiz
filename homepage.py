import tkinter as tk
import subprocess
import sys

class HomePage:
    def __init__(self, root, username):
        self.root = root
        self.username = username  # Store the username for future reference
        self.root.title(f"Quiz App - Home ({username})")

        # Welcome Label
        welcome_label = tk.Label(root, text=f"Welcome {username} to the Quiz App!", font=("Arial", 18))
        welcome_label.pack(pady=20)

        # Subject Selection
        subject_label = tk.Label(root, text="Select Subject:", font=("Arial", 14))
        subject_label.pack(pady=10)
        
        subjects = ["OOP", "Python", "Java", "C++"]
        for subject in subjects:
            button = tk.Button(root, text=subject, font=("Arial", 12), command=lambda s=subject: self.start_quiz(s))
            button.pack(pady=5)

        # Account Section
        account_button = tk.Button(root, text="Account", font=("Arial", 12), command=self.show_account)
        account_button.pack(pady=20)

    def start_quiz(self, subject):
        self.root.destroy()  # Close the home page interface
        # Use the correct Python executable
        python_executable = sys.executable
        subprocess.call([python_executable, "quizpage.py", subject, self.username])  # Open the quiz page interface for the selected subject

    def show_account(self):
        # Display account information (to be implemented)
        pass

if __name__ == "__main__":
    username = sys.argv[1] if len(sys.argv) > 1 else "User"  # Get the username from the command line arguments
    root = tk.Tk()
    home_page = HomePage(root, username)
    root.mainloop()
