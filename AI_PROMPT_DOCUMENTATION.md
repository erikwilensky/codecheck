# AI Quiz Generation - Code Documentation

This document shows exactly what code and prompts are sent to the AI when generating quiz questions.

## Overview

The AI receives:
1. **System prompt** - Instructions for the AI's role
2. **User prompt** - Detailed instructions with code content
3. **Function schema** - JSON structure for responses
4. **Code content** - Student's actual code

## 1. System Prompt

```python
{
    "role": "system", 
    "content": "You are an expert programming instructor creating comprehension and application quiz questions. Format as numbered questions (1-5) with relevant code snippets included. No answer spaces after individual questions - just questions and code snippets."
}
```

## 2. User Prompt Structure

The user prompt is built by `_create_prompt()` method in `QuizGenerationService`:

```python
def _create_prompt(self, code_content: str, assignment_name: str) -> str:
    """Create a simple prompt for quiz generation."""
    return f"""
Create 5 simple comprehension and application quiz questions for a {assignment_name} assignment.

CODE TO ANALYZE:
{code_content[:2000]}

REQUIREMENTS:
- Questions must reference specific code snippets from the student's actual code
- Include the relevant code snippet with each question
- Focus on comprehension (understanding why) and application (how to modify/extend)
- Avoid generic questions that could apply to any code
- Include questions about design decisions, error handling, and code structure
- Questions should be medium to hard difficulty
- Each question should test a different aspect of the code
- Format as numbered questions (1-5) with code snippets included
- No answer spaces after individual questions - just the questions and code snippets
- Questions should be open-ended and require explanation

Generate questions that prove the student understands their own implementation.
"""
    return prompt
```

## 3. Function Calling Schema

The AI must respond using this exact JSON structure:

```json
{
    "name": "create_quiz",
    "description": "Return 5-7 quiz questions that probe the student's understanding of their own code.",
    "parameters": {
        "type": "object",
        "properties": {
            "questions": {
                "type": "array",
                "items": {
                    "type": "object",
                    "properties": {
                        "question_text": {"type": "string"},
                        "code_snippet": {"type": "string"},
                        "explanation": {"type": "string"}
                    },
                    "required": ["question_text"]
                },
                "minItems": 5,
                "maxItems": 7
            }
        },
        "required": ["questions"]
    }
}
```

## 4. Complete API Call

```python
response = await asyncio.to_thread(
    self.client.chat.completions.create,
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": "You are an expert programming instructor creating comprehension/application quiz questions."
        },
        {
            "role": "user",
            "content": prompt  # The detailed prompt with code
        }
    ],
    functions=[function_schema],  # The JSON schema above
    function_call={"name": "create_quiz"},
    temperature=0.6,
    max_tokens=1200
)
```

## 5. Example: Voting Booth Assignment

When a student submits a voting booth assignment, the AI receives:

### System Message
```
You are an expert programming instructor creating comprehension/application quiz questions.
```

### User Message
```
Create 5-7 comprehension and application quiz questions for a student's Voting Booth assignment.

Focus on questions that test if the student actually wrote and understands their code, not memorization.

Student's Code:
import tkinter as tk
from tkinter import messagebox
import sqlite3

class VotingBooth:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Voting Booth")
        self.root.geometry("400x300")
        
        # Database setup
        self.conn = sqlite3.connect('voting.db')
        self.cursor = self.conn.cursor()
        self.setup_database()
        
        # UI setup
        self.setup_ui()
    
    def setup_database(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS voters (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                has_voted BOOLEAN DEFAULT FALSE
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidates (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                votes INTEGER DEFAULT 0
            )
        ''')
        self.conn.commit()
    
    def setup_ui(self):
        # Voter ID entry
        tk.Label(self.root, text="Voter ID:").pack(pady=5)
        self.voter_id = tk.Entry(self.root)
        self.voter_id.pack(pady=5)
        
        # Candidate selection
        tk.Label(self.root, text="Select Candidate:").pack(pady=5)
        self.candidate_var = tk.StringVar()
        candidates = ["Candidate A", "Candidate B", "Candidate C"]
        for candidate in candidates:
            tk.Radiobutton(self.root, text=candidate, variable=self.candidate_var, 
                          value=candidate).pack()
        
        # Vote button
        tk.Button(self.root, text="Submit Vote", command=self.submit_vote).pack(pady=20)
        
        # Results button
        tk.Button(self.root, text="Show Results", command=self.show_results).pack(pady=5)
    
    def submit_vote(self):
        voter_id = self.voter_id.get()
        candidate = self.candidate_var.get()
        
        if not voter_id or not candidate:
            messagebox.showerror("Error", "Please enter voter ID and select candidate")
            return
        
        # Check if voter has already voted
        self.cursor.execute("SELECT has_voted FROM voters WHERE id = ?", (voter_id,))
        result = self.cursor.fetchone()
        
        if result and result[0]:
            messagebox.showerror("Error", "Voter has already voted")
            return
        
        # Record vote
        self.cursor.execute("INSERT OR REPLACE INTO voters (id, name, has_voted) VALUES (?, ?, TRUE)", 
                          (voter_id, f"Voter_{voter_id}"))
        self.cursor.execute("UPDATE candidates SET votes = votes + 1 WHERE name = ?", (candidate,))
        self.conn.commit()
        
        messagebox.showinfo("Success", "Vote recorded successfully!")
        self.voter_id.delete(0, tk.END)
        self.candidate_var.set("")
    
    def show_results(self):
        self.cursor.execute("SELECT name, votes FROM candidates ORDER BY votes DESC")
        results = self.cursor.fetchall()
        
        result_text = "Election Results:\n\n"
        for candidate, votes in results:
            result_text += f"{candidate}: {votes} votes\n"
        
        messagebox.showinfo("Results", result_text)
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = VotingBooth()
    app.run()

Requirements:
- Questions must reference specific code snippets from the student's actual code
- Focus on comprehension (understanding why) and application (how to modify/extend)
- Avoid generic questions that could apply to any code
- Include questions about design decisions, error handling, and code structure
- Questions should be medium to hard difficulty
- Each question should test a different aspect of the code

Generate questions that prove the student understands their own implementation.
```

## 6. Expected AI Response

The AI should respond with a function call containing JSON like this:

```json
{
    "questions": [
        {
            "question_type": "code_explanation",
            "question_text": "Why did you use a boolean field 'has_voted' in the voters table instead of just checking if a voter ID exists?",
            "code_snippet": "has_voted BOOLEAN DEFAULT FALSE",
            "options": [],
            "correct_answer": "To distinguish between registered voters who haven't voted yet and those who have already voted, preventing duplicate votes.",
            "difficulty": "medium",
            "learning_objectives": ["database_design", "data_integrity"],
            "explanation": "This design choice prevents the same voter from voting multiple times while allowing voters to be pre-registered."
        },
        {
            "question_type": "code_application",
            "question_text": "How would you modify your voting system to support multiple elections running simultaneously?",
            "code_snippet": "CREATE TABLE IF NOT EXISTS candidates (id INTEGER PRIMARY KEY, name TEXT NOT NULL, votes INTEGER DEFAULT 0)",
            "options": [],
            "correct_answer": "Add an 'election_id' field to both tables and modify queries to filter by election_id.",
            "difficulty": "hard",
            "learning_objectives": ["database_normalization", "system_design"],
            "explanation": "This requires understanding database relationships and how to extend the current schema."
        }
    ]
}
```

## 7. Error Handling

The system includes guards against common failures:

```python
# Guard against silent schema mismatch
choice = response.choices[0]
if not choice.message.function_call:
    raise RuntimeError("Model did not call the function; falling back to plain text.")

# Parse function call arguments (guaranteed JSON)
function_args = choice.message.function_call.arguments
quiz_data = json.loads(function_args)
```

## 8. Token Management

- **Content trimming**: Code is limited to 2000 characters
- **Max tokens**: 1200 for response
- **Temperature**: 0.6 for balanced creativity/consistency

## 9. Key Features

✅ **Function calling** - Guaranteed JSON responses  
✅ **Code-specific questions** - References actual student code  
✅ **Comprehension focus** - Tests understanding, not memorization  
✅ **No fallbacks** - Clean failure instead of generic questions  
✅ **Rich schema** - Includes difficulty, objectives, explanations  

This ensures the AI generates high-quality, code-specific questions that truly test student comprehension and application of their own code. 