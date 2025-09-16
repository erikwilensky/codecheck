import json
import asyncio
from typing import List, Dict, Any
from pydantic import BaseModel
from ..services.openai_client import get_client_or_none

class QuizQuestion(BaseModel):
    question: str
    code_snippet: str
    focus: str

class QuizGenerationService:
    """Dedicated service for generating quiz questions from code analysis."""
    
    QUIZ_SCHEMA = {
        "type": "object",
        "properties": {
            "quiz_text": {"type": "string"},
        },
        "required": ["quiz_text"]
    }
    
    def __init__(self):
        self.client = get_client_or_none()
    
    async def generate_quiz_questions(self, code_content: str, assignment_name: str) -> List[QuizQuestion]:
        """Generate quiz questions using OpenAI with function calling for reliable JSON."""
        
        if not self.client:
            raise RuntimeError("OpenAI API key not configured - quiz generation unavailable")
        
        try:
            # Log the exact schema being sent
            function_schema = {
                "name": "create_quiz",
                "description": "Return a block of text containing 5 quiz questions.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "quiz_text": {
                            "type": "string",
                            "description": "A block of text containing 5 numbered questions based on the provided code."
                        }
                    },
                    "required": ["quiz_text"]
                }
            }
            
            print(f"DEBUG function_schema: {json.dumps(function_schema, indent=2)}")
            print(f"DEBUG function_call: {{'name': 'create_quiz'}}")
            print(f"DEBUG client type: {type(self.client)}")
            print(f"DEBUG client has 'chat': {hasattr(self.client, 'chat')}")
            print(f"DEBUG client has 'ChatCompletion': {hasattr(self.client, 'ChatCompletion')}")
            
            # Use function calling for guaranteed JSON response
            # Check if we have the modern SDK or legacy SDK
            # Modern SDK has 'chat' attribute, legacy SDK has 'ChatCompletion'
            if hasattr(self.client, 'chat') and not hasattr(self.client, 'ChatCompletion'):
                # Modern SDK (openai>=1.x)
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are an expert programming instructor creating quiz questions to verify that beginner Python students actually wrote and understand their own code. Return ONLY 5 numbered questions (1-5) as plain text with no answer spaces or explanations."
                        },
                        {
                            "role": "user",
                            "content": self._create_prompt(code_content, assignment_name)
                        }
                    ],
                    tools=[{
                        "type": "function",
                        "function": function_schema
                    }],
                    tool_choice={"type": "function", "function": {"name": "create_quiz"}},
                    temperature=0.6,
                    max_tokens=1200
                )
            else:
                # Legacy SDK (openai==0.x)
                response = self.client.ChatCompletion.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system", 
                            "content": "You are an expert programming instructor creating quiz questions to verify that beginner Python students actually wrote and understand their own code. Return ONLY 5 numbered questions (1-5) as plain text with no answer spaces or explanations."
                        },
                        {
                            "role": "user",
                            "content": self._create_prompt(code_content, assignment_name)
                        }
                    ],
                    functions=[function_schema],
                    function_call={"name": "create_quiz"},
                    temperature=0.6,
                    max_tokens=1200
                )
            
            # Guard against silent schema mismatch
            choice = response.choices[0]
            
            # Debug: Log the raw message
            print(f"DEBUG raw message: {choice.message}")
            
            # Handle both modern and legacy API formats
            if hasattr(self.client, 'chat') and not hasattr(self.client, 'ChatCompletion'):
                # Modern SDK - check for tool calls
                print(f"DEBUG tool_calls: {choice.message.tool_calls}")
                print(f"DEBUG content: {choice.message.content}")
                
                if choice.message.content and not choice.message.tool_calls:
                    raise RuntimeError(
                        "Model returned plain text instead of calling create_quiz:\n"
                        f"{choice.message.content[:200]}..."
                    )

                if not choice.message.tool_calls:
                    raise RuntimeError("No tool_calls — schema mismatch or wrong model")
                
                # Parse tool call arguments (guaranteed JSON)
                function_args = choice.message.tool_calls[0].function.arguments
                quiz_data = json.loads(function_args)
            else:
                # Legacy SDK - check for function calls
                print(f"DEBUG function_call: {choice.message.function_call}")
                print(f"DEBUG content: {choice.message.content}")
                
                if choice.message.content and not choice.message.function_call:
                    raise RuntimeError(
                        "Model returned plain text instead of calling create_quiz:\n"
                        f"{choice.message.content[:200]}..."
                    )

                if not choice.message.function_call:
                    raise RuntimeError("No function_call — schema mismatch or wrong model")
                
                # Parse function call arguments (guaranteed JSON)
                function_args = choice.message.function_call.arguments
                quiz_data = json.loads(function_args)
            
            # Convert to QuizQuestion objects
            questions = []
            quiz_text = quiz_data.get("quiz_text", "")
            
            # Use regex to properly parse questions with code snippets
            import re
            
            pattern = re.compile(
                r"(?P<num>\d\.) (?P<question>.*?)\s*Code snippet:\s*(?P<snippet>.*?)(?=\n\d\.|\Z)",
                re.DOTALL
            )
            
            for match in pattern.finditer(quiz_text.strip()):
                question_text = match.group("question").strip()
                code_snippet = match.group("snippet").strip()
                
                print(f"DEBUG: Parsed question: {question_text[:50]}...")
                print(f"DEBUG: Parsed snippet: {code_snippet[:50]}...")
                
                questions.append(QuizQuestion(
                    question=question_text,
                    code_snippet=code_snippet,
                    focus="Comprehension"
                ))
            
            return questions[:5]  # Ensure exactly 5 questions
            
        except Exception as e:
            print(f"AI quiz generation failed: {e}")
            raise RuntimeError(f"Quiz generation failed: {str(e)}")
    
    def _create_prompt(self, code_content: str, assignment_name: str) -> str:
        """Create a simple prompt for quiz generation."""
        return f"""
You are an expert programming instructor creating quiz questions to verify that beginner Python students actually wrote and understand their own code.

Your task is to read the code below and write 5 thoughtful quiz questions that test the student's understanding of their own implementation.

📋 Guidelines:

Each question must refer directly to a specific part of the code and include a short, relevant code snippet (max 6 lines) to illustrate what it asks about.

Format: First the question, then on the next line write:
Code snippet:
followed by the snippet itself, on a separate indented line.

Focus on comprehension, reasoning, and application — NOT memorization.
Do NOT ask generic questions that could apply to any code — base all questions on the actual code you see.
Write the questions as plain numbered text (1–5). No answers, no blanks, no explanations.

Here is the student's code:
{code_content[:2000]}
"""
    
# No fallback questions - fail cleanly if AI is unavailable 