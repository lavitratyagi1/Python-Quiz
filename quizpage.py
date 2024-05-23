import sys
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import subprocess
import sys

# Database connection details
DB_HOST = "localhost"
DB_USER = "lavitra"
DB_PASSWORD = "1234567890"
DB_NAME = "oops_project"

# Establish connection to the MySQL database
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
cur = conn.cursor()

class QuizApp:
    def __init__(self, root, subject, username):
        self.root = root
        self.subject = subject  # Store the selected subject
        self.username = username  # Store the username
        self.current_question_index = 0
        self.correct_answered = 0  # Track correct answers
        self.wrong_answered = 0  # Track wrong answers
        self.total_questions = 0  # Total number of questions
        self.score = 0  # Initialize the score
        
        # Fetch questions for the selected subject from the database
        self.questions = self.load_questions()
        self.total_questions = len(self.questions)  # Set the total number of questions
        
        # Create a Canvas widget for the background image
        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()
        self.background_image = tk.PhotoImage(file="/home/lavitra/Desktop/coding/python/Python-Quiz/tim1.png")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)
        
        self.question_label = tk.Label(self.canvas, text="", font=("Arial", 14), bg='white')
        self.question_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)
        
        self.score_label = tk.Label(self.canvas, text=f"Score: {self.score}", font=("Arial", 14), bg='white')
        self.score_label.place(relx=0.97, rely=0.05, anchor=tk.E)

        self.option_buttons = []
        for i in range(4):
            button = tk.Button(self.canvas, text="", font=("Arial", 12))
            button.place(relx=0.5, rely=0.3 + i*0.1, anchor=tk.CENTER)
            button.bind("<Button-1>", self.check_answer)  # Bind left mouse button click event
            self.option_buttons.append(button)

        self.display_question()

    def load_questions(self):
        table_name = f"{self.subject.lower()}_questions"
        cur.execute(f"SELECT question, option_a, option_b, option_c, option_d, correct_answer, level FROM {table_name} ORDER BY level")
        return cur.fetchall()

    def display_question(self):
        if self.current_question_index < self.total_questions:
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question[0])
            for i in range(4):
                self.option_buttons[i].config(text=question[i+1], relief=tk.RAISED)  # Reset button appearance
        else:
            self.show_results()

    def check_answer(self, event):
        clicked_button = event.widget
        reply = clicked_button.cget("text")[0]  # Extracting the first character from the button text
        question = self.questions[self.current_question_index]
        if reply == question[5]:
            messagebox.showinfo("Correct", "Correct answer!")
            self.correct_answered += 1
            self.score += 1000  # Increase the score by 1000 points for each correct answer
        else:
            messagebox.showerror("Wrong", "Wrong answer")
            self.wrong_answered += 1
        
        self.update_score_label()  # Update the score display
        self.root.after(1000, self.next_question)  # Automatically move to the next question after 1 second

    def next_question(self):
        self.current_question_index += 1
        self.display_question()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

    def show_results(self):
        messagebox.showinfo("Quiz Results",
                            f"Quiz completed!\n\n"
                            f"Total questions: {self.total_questions}\n"
                            f"Correct answers: {self.correct_answered}\n"
                            f"Wrong answers: {self.wrong_answered}\n"
                            f"Final Score: {self.score}")
        self.save_score()
        self.root.destroy()
        python_executable = sys.executable
        subprocess.call([python_executable, "homepage.py", username])  # Open the homepage interface with username

    def save_score(self):
        cur.execute("SELECT score FROM scores WHERE username = %s", (self.username,))
        result = cur.fetchone()
        if result:
            new_score = result[0] + self.score
            cur.execute("UPDATE scores SET score = %s WHERE username = %s", (new_score, self.username))
        else:
            cur.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (self.username, self.score))
        conn.commit()

if __name__ == "__main__":
    subject = sys.argv[1] if len(sys.argv) > 1 else "Unknown"
    username = sys.argv[2] if len(sys.argv) > 2 else "User"
    root = tk.Tk()
    app = QuizApp(root, subject, username)
    root.mainloop()

    # Close the database connection when done
    cur.close()
    conn.close()
