import tkinter as tk #all my imports
from tkinter import messagebox
import sqlite3
import random


conn = sqlite3.connect('voting_booth.db')  #this is for the initialization of the database
cursor = conn.cursor()


# this it to make a random voter id
def generate_voter_id():
    while True:
        voter_id = str(random.randint(10000, 99999))
        cursor.execute('SELECT * FROM voters WHERE voter_id = ?', (voter_id,)) #found this select * from some utube vid seemed pretty useful i continue to use later on
        if not cursor.fetchone():
            return voter_id


def register_voter(): #voter registation interface
    def submit_registration():
        first_name = entry_first_name.get()
        last_name = entry_last_name.get()
        party = entry_party.get()

        if first_name and last_name and party:
            voter_id = generate_voter_id()
            cursor.execute('INSERT INTO voters (voter_id, first_name, last_name, party) VALUES (?, ?, ?, ?)',
                           (voter_id, first_name, last_name, party))
            conn.commit()  #saves all changes
            messagebox.showinfo("Registration Success", f"Your voter ID is: {voter_id}\nKeep it safe to vote.")
            entry_first_name.delete(0, tk.END)
            entry_last_name.delete(0, tk.END)
            entry_party.delete(0, tk.END)
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    window = tk.Tk()
    window.geometry("500x400")
    window.title("Voter Registration")

    tk.Label(window, text="First Name:", font=("Times New Roman", 20)).grid(row=0, column=0, padx=20, pady=20)
    tk.Label(window, text="Last Name:", font=("Times New Roman", 20)).grid(row=1, column=0, padx=20, pady=20)
    tk.Label(window, text="Grade Level:", font=("Times New Roman", 20)).grid(row=2, column=0, padx=20, pady=20)

    entry_first_name = tk.Entry(window, font=("Times New Roman", 20), width=20)
    entry_last_name = tk.Entry(window, font=("Times New Roman", 20), width=20)
    entry_party = tk.Entry(window, font=("Times New Roman", 20), width=20)

    entry_first_name.grid(row=0, column=1, padx=20, pady=20)
    entry_last_name.grid(row=1, column=1, padx=20, pady=20)
    entry_party.grid(row=2, column=1, padx=20, pady=20)

    tk.Button(window, text="Register", command=submit_registration, font=("Times New Roman", 14), width=15).grid(row=3, columnspan=2, pady=20)
    window.mainloop()


def vote(): #this is the voter interface
    def submit_vote():
        voter_id = entry_voter_id.get()
        subject = selected_subject.get()

        cursor.execute('SELECT * FROM voters WHERE voter_id = ?', (voter_id,)) #took from a utube vid
        voter = cursor.fetchone() #to retrieve the vote

        if voter:
            cursor.execute('SELECT * FROM votes WHERE voter_id = ?', (voter_id,))
            if cursor.fetchone():
                messagebox.showwarning("Vote Error", "You have already voted!")
            else:
                cursor.execute('INSERT INTO votes (voter_id, subject) VALUES (?, ?)', (voter_id, subject))
                conn.commit()
                messagebox.showinfo("Vote Successful", "Thank you for voting!")
                entry_voter_id.delete(0, tk.END)
        else:
            messagebox.showwarning("Vote Error", "Invalid voter ID!")

    window = tk.Tk()
    window.geometry("500x350")
    window.title("Vote for Hardest IB Subject")

    tk.Label(window, text="Enter Voter ID:", font=("Times New Roman", 14)).grid(row=0, column=0, padx=20, pady=20)
    entry_voter_id = tk.Entry(window, font=("Times New Roman", 14), width=20)
    entry_voter_id.grid(row=0, column=1, padx=20, pady=20)

    selected_subject = tk.StringVar()
    selected_subject.set("HL AA Math")

    tk.Radiobutton(window, text="HL AA Math", variable=selected_subject, value="HL AA Math", font=("Times New Roman", 14)).grid(row=1, column=0, padx=20, pady=20)
    tk.Radiobutton(window, text="HL Physics", variable=selected_subject, value="HL Physics", font=("Times New Roman", 14)).grid(row=1, column=1, padx=20, pady=20)

    tk.Button(window, text="Submit Vote", command=submit_vote, font=("Times New Roman", 14), width=15).grid(row=2, columnspan=2, pady=20)
    window.mainloop()


def count_votes(): #this is to show the voter count for the last part
    cursor.execute('SELECT subject, COUNT(*) FROM votes GROUP BY subject')
    results = cursor.fetchall() #to retrieve all the rows from the tuples

    if not results:
        messagebox.showinfo("No Votes", "No votes have been cast yet.")
        return

    window = tk.Tk()
    window.geometry("500x300")
    window.title("Vote Results")

    result_text = "Vote Results:\n\n"
    for subject, count in results:
        result_text += f"{subject}: {count} votes\n"

    tk.Label(window, text=result_text, font=("Times New Roman", 20)).pack(pady=40)
    window.mainloop()


def main_menu(): #interface for the main menu
    window = tk.Tk()
    window.geometry("500x400")
    window.title("Subject Voting Machine")

    tk.Button(window, text="Register Voter", command=register_voter, font=("Times New Roman", 20), width=40).pack(pady=40)
    tk.Button(window, text="Vote", command=vote, font=("Times New Roman", 20), width=40).pack(pady=40)
    tk.Button(window, text="Count Votes", command=count_votes, font=("Times New Roman", 20), width=40).pack(pady=40)

    window.mainloop()

if __name__ == "__main__":
    main_menu()
