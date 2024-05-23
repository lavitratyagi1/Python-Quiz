import tkinter as tk
from tkinter import messagebox
import mysql.connector

# Database connection details
DB_HOST = "localhost"
DB_USER = "lavitra"
DB_PASSWORD = "1234567890"
DB_NAME = "oops_project"

# Establish connection to the MySQL database
conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
cur = conn.cursor()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.current_question_index = 0
        self.correct_answered = False  # Flag to track if the answer is correct
        self.username = "User"  # Placeholder for user's name
        self.score = 0  # Initialize the score
        
        # Fetch questions from the database
        self.questions = self.load_questions()
        
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
        cur.execute("SELECT question, option_a, option_b, option_c, option_d, correct_answer, level FROM questions ORDER BY level")
        questions = cur.fetchall()
        return questions

    def display_question(self):
        if self.current_question_index < len(self.questions):
            question = self.questions[self.current_question_index]
            self.question_label.config(text=question[0])
            for i in range(4):
                self.option_buttons[i].config(text=question[i+1], relief=tk.RAISED)  # Reset button appearance
        else:
            messagebox.showinfo("End of Quiz", "Congratulations! You have completed the quiz.")
            self.save_score()
            self.root.quit()

    def check_answer(self, event):
        if self.correct_answered:
            # If already answered correctly, ignore further submissions
            return
        
        clicked_button = event.widget
        reply = clicked_button.cget("text")[0]  # Extracting the first character from the button text
        question = self.questions[self.current_question_index]
        if reply == question[5]:
            messagebox.showinfo("Correct", "Correct answer!")
            self.correct_answered = True  # Set the flag to True
            self.score += 1000  # Increase the score by 1000 points for each correct answer
            self.update_score_label()  # Update the score display
            self.root.after(1000, self.next_question)  # Automatically move to the next question after 1 second
        else:
            messagebox.showerror("Wrong", "Wrong answer")
            self.save_score()
            self.root.quit()  # Quit the application if the answer is wrong

    def next_question(self):
        self.current_question_index += 1
        self.correct_answered = False  # Reset the flag
        self.display_question()

    def save_score(self):
        cur.execute("INSERT INTO scores (username, score) VALUES (%s, %s)", (self.username, self.score))
        conn.commit()

    def update_score_label(self):
        self.score_label.config(text=f"Score: {self.score}")

root = tk.Tk()
app = QuizApp(root)
root.mainloop()

# Close the database connection when done
cur.close()
conn.close()