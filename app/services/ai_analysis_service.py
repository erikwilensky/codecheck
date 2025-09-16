import os
from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models import Submission, Analysis, Quiz, QuizQuestion, Student
from datetime import datetime
import json
from .openai_client import get_client_or_none

class AIAnalysisService:
    def __init__(self):
        self.openai_client = get_client_or_none()
    
    def analyze_submission_with_ai(self, submission: Submission, db: Session) -> Analysis:
        """Use OpenAI to analyze code submission"""
        
        # Get student's submission history for context
        submission_history = self._get_submission_history(submission.student_id, db)
        
        # Prepare comprehensive context including history
        analysis_context = self._prepare_analysis_context(submission, submission_history)
        
        # Get AI analysis with historical context
        ai_analysis = self._get_ai_analysis_with_history(analysis_context)
        
        # Create analysis record
        analysis = Analysis(
            student_id=submission.student_id,
            submission_id=submission.id,
            analysis_type='ai_enhanced_with_history',
            status='completed',
            results=ai_analysis,
            confidence_score=ai_analysis.get('confidence_score', 0.8),
            completed_at=datetime.utcnow()
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return analysis
    
    def _get_submission_history(self, student_id: int, db: Session) -> List[Dict[str, Any]]:
        """Get student's submission history for context"""
        submissions = db.query(Submission).filter(
            Submission.student_id == student_id
        ).order_by(Submission.created_at.desc()).limit(10).all()
        
        history = []
        for sub in submissions:
            history.append({
                'assignment_name': sub.assignment_name,
                'file_name': sub.file_name,
                'file_size': sub.file_size,
                'created_at': sub.created_at.isoformat() if sub.created_at else None
            })
        
        return history
    
    def _prepare_analysis_context(self, submission: Submission, history: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Prepare comprehensive context including historical data"""
        return {
            'current_submission': {
                'assignment_name': submission.assignment_name,
                'file_name': submission.file_name,
                'file_content': submission.file_content,
                'file_size': submission.file_size,
                'created_at': submission.created_at.isoformat() if submission.created_at else None
            },
            'submission_history': history,
            'analysis_parameters': {
                'history_length': len(history),
                'time_span_days': self._calculate_time_span(history),
                'total_submissions': len(history) + 1
            }
        }
    
    def _calculate_time_span(self, history: List[Dict[str, Any]]) -> int:
        """Calculate time span of submission history in days"""
        if len(history) < 2:
            return 0
        
        try:
            first_date = datetime.fromisoformat(history[-1]['created_at'])
            last_date = datetime.fromisoformat(history[0]['created_at'])
            return (last_date - first_date).days
        except:
            return 0
    
    def _get_ai_analysis_with_history(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Use OpenAI to analyze submission with historical context"""
        
        current = context['current_submission']
        history = context['submission_history']
        
        # Create detailed prompt with historical context
        prompt = f"""
        Analyze this code submission with its complete historical context for learning assessment:

        **CURRENT SUBMISSION:**
        Assignment: {current['assignment_name']}
        File: {current['file_name']}
        File Size: {current['file_size']} bytes
        Date: {current['created_at']}

        **SUBMISSION HISTORY (Last {len(history)} submissions):**
        """
        
        # Add historical context
        for i, hist_sub in enumerate(history):
            prompt += f"""
        Submission {i+1} ({hist_sub['created_at']}):
        - Assignment: {hist_sub['assignment_name']}
        - File: {hist_sub['file_name']}
        - Size: {hist_sub['file_size']} bytes
        """
        
        prompt += f"""
        
        **ANALYSIS REQUIREMENTS:**
        
        1. **Learning Progression Analysis**:
           - Compare current submission with historical pattern
           - Identify gradual vs sudden improvements
           - Assess consistency in coding style and approach
           - Detect learning plateaus or regressions
        
        2. **Tool Dependency Detection**:
           - Look for patterns across multiple submissions
           - Identify inconsistencies that suggest tool usage
           - Compare assignment complexity over time
           - Detect sudden changes in coding sophistication
        
        3. **Knowledge Consistency Assessment**:
           - Check if understanding level is consistent across submissions
           - Identify gaps between advanced concepts and foundational knowledge
           - Detect copy-paste patterns across multiple submissions
           - Assess whether improvements are gradual or artificial
        
        4. **Authentic Learning Indicators**:
           - Gradual skill development over time
           - Consistent problem-solving approaches
           - Natural progression in code complexity
           - Genuine understanding vs memorization
        
        **HISTORICAL PATTERN ANALYSIS:**
        - Time span: {context['analysis_parameters']['time_span_days']} days
        - Total submissions: {context['analysis_parameters']['total_submissions']}
        - Learning trajectory assessment
        - Consistency evaluation across submissions
        
        Return your analysis as a JSON object with this structure:
        {{
            "historical_analysis": {{
                "learning_trajectory": "gradual|sudden|plateau|regression",
                "consistency_score": 0.0,
                "improvement_rate": 0.0,
                "pattern_anomalies": [],
                "time_based_analysis": {{
                    "regular_submissions": true,
                    "submission_frequency": "consistent|irregular",
                    "quality_progression": "steady|volatile|declining"
                }}
            }},
            "tool_dependency": {{
                "ai_usage_probability": 0.0,
                "copilot_usage_probability": 0.0,
                "copy_paste_probability": 0.0,
                "historical_indicators": [],
                "consistency_analysis": {{
                    "style_consistency": 0.0,
                    "knowledge_consistency": 0.0,
                    "progress_consistency": 0.0
                }},
                "confidence": 0.0
            }},
            "learning_progression": {{
                "overall_progression": "positive|negative|neutral",
                "skill_development_rate": 0.0,
                "understanding_level": "beginner|intermediate|advanced",
                "learning_gaps": [],
                "strengths": [],
                "areas_for_improvement": []
            }},
            "authentic_learning_assessment": {{
                "authentic_learning_score": 0.0,
                "genuine_understanding": true,
                "gradual_improvement": true,
                "consistent_approach": true,
                "red_flags": [],
                "green_flags": []
            }},
            "intervention_recommendations": {{
                "intervention_needed": false,
                "intervention_type": "none|understanding_check|foundational_review|advanced_challenge",
                "specific_recommendations": [],
                "priority": "low|medium|high"
            }},
            "confidence_score": 0.0
        }}
        """
        
        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert educational assessment system that analyzes code submission history to detect authentic learning vs tool dependency. Focus on patterns, consistency, and gradual progression over time."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            analysis_result = json.loads(ai_response)
            
            # Add metadata
            analysis_result['ai_analysis_timestamp'] = datetime.utcnow().isoformat()
            analysis_result['analysis_method'] = 'openai_gpt4_with_history'
            analysis_result['history_context'] = {
                'submissions_analyzed': len(history) + 1,
                'time_span_days': context['analysis_parameters']['time_span_days']
            }
            
            return analysis_result
            
        except Exception as e:
            # Fallback to basic analysis if AI fails
            return self._fallback_analysis_with_history(context)
    
    def _fallback_analysis_with_history(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Fallback analysis with historical context if AI fails"""
        return {
            "historical_analysis": {
                "learning_trajectory": "unknown",
                "consistency_score": 0.5,
                "improvement_rate": 0.0,
                "pattern_anomalies": ["AI analysis unavailable"],
                "time_based_analysis": {
                    "regular_submissions": True,
                    "submission_frequency": "unknown",
                    "quality_progression": "unknown"
                }
            },
            "tool_dependency": {
                "ai_usage_probability": 0.0,
                "copilot_usage_probability": 0.0,
                "copy_paste_probability": 0.0,
                "historical_indicators": ["AI analysis unavailable"],
                "consistency_analysis": {
                    "style_consistency": 0.5,
                    "knowledge_consistency": 0.5,
                    "progress_consistency": 0.5
                },
                "confidence": 0.0
            },
            "learning_progression": {
                "overall_progression": "unknown",
                "skill_development_rate": 0.0,
                "understanding_level": "unknown",
                "learning_gaps": ["AI analysis unavailable"],
                "strengths": [],
                "areas_for_improvement": []
            },
            "authentic_learning_assessment": {
                "authentic_learning_score": 0.5,
                "genuine_understanding": True,
                "gradual_improvement": True,
                "consistent_approach": True,
                "red_flags": [],
                "green_flags": []
            },
            "intervention_recommendations": {
                "intervention_needed": False,
                "intervention_type": "none",
                "specific_recommendations": ["AI analysis service unavailable"],
                "priority": "low"
            },
            "confidence_score": 0.0,
            "ai_analysis_timestamp": datetime.utcnow().isoformat(),
            "analysis_method": "fallback_with_history",
            "error": "AI analysis failed"
        }
    
    def generate_ai_quiz(self, submission: Submission, analysis: Analysis, db: Session) -> Quiz:
        """Use OpenAI to generate personalized quiz based on historical analysis"""
        
        # Get submission history for quiz context
        submission_history = self._get_submission_history(submission.student_id, db)
        
        # Create quiz record
        quiz = Quiz(
            student_id=submission.student_id,
            submission_id=submission.id,
            quiz_type='ai_generated_with_history',
            status='generated',
            total_questions=0,
            created_at=datetime.utcnow()
        )
        
        db.add(quiz)
        db.commit()
        db.refresh(quiz)
        
        # Generate AI-powered questions with historical context
        questions = self._generate_ai_questions_with_history(submission, analysis, submission_history)
        
        # Add questions to database
        for question_data in questions:
            question = QuizQuestion(
                quiz_id=quiz.id,
                **question_data
            )
            db.add(question)
        
        # Update quiz with question count
        quiz.total_questions = len(questions)
        db.commit()
        db.refresh(quiz)
        
        return quiz
    
    def _generate_ai_questions_with_history(self, submission: Submission, analysis: Analysis, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Use OpenAI to generate personalized quiz questions with historical context"""
        
        analysis_results = analysis.results
        
        # Create context for quiz generation
        history_summary = self._create_history_summary(history)
        
        prompt = f"""
        You are an expert programming instructor creating a quiz to verify a student's understanding of their own code submission. Your goal is to determine if they genuinely wrote and understand the code.

        **CODE SUBMISSION TO ANALYZE:**
        - Assignment: {submission.assignment_name}
        - File Name: {submission.file_name}
        ```python
        {submission.file_content}
        ```

        **HISTORICAL CONTEXT (Previous Submissions):**
        {history_summary}

        **AI ANALYSIS OF THIS SUBMISSION:**
        - Learning Trajectory: {analysis_results.get('historical_analysis', {}).get('learning_trajectory', 'unknown')}
        - Understanding Level: {analysis_results.get('learning_progression', {}).get('understanding_level', 'unknown')}
        - Suspected AI/Tool Usage: {analysis_results.get('tool_dependency', {}).get('confidence', 0.0) > 0.5}

        **QUIZ REQUIREMENTS:**
        Generate exactly 5-7 quiz questions that probe the student's deep understanding of the provided code. The questions MUST cover the following categories:

        1.  **Logic Flow (1-2 questions):** Ask about the `if/else` conditions, loops, or boolean logic. Why was a certain path taken?
            *Example: "In the `divide` function, what is the purpose of the `if b == 0:` check?"*

        2.  **Procedures/Functions (1-2 questions):** Ask about the purpose of a function, its parameters, or its return value.
            *Example: "What does the `calculator` function return if the user enters '5' as their choice?"*

        3.  **Statements/Variables (1-2 questions):** Ask about a specific line of code or the purpose of a variable.
            *Example: "On line 23, what is the data type of the `num1` variable after the input is received?"*

        4.  **Extrapolation / "What If" (1-2 questions):** Ask what would happen if a specific line of code were changed. This tests for robust understanding.
            *Example: "What would happen if you removed the `float()` conversion from the input on lines 22 and 23?"*
            
        5.  **Technique/Approach (1 question):** Ask why a particular programming technique was used.
            *Example: "Why did you choose to create separate functions like `add` and `subtract` instead of putting the logic directly inside the `if/elif` statements?"*

        **OUTPUT FORMAT:**
        Return ONLY a valid JSON array of question objects. Do not include any other text or explanations.
        [
            {{
                "question_type": "multiple_choice|code_explanation|debugging|problem_solving",
                "question_text": "Question text here",
                "code_snippet": "A relevant, short code snippet from the file, if applicable.",
                "options": ["Option A", "Option B", "Option C", "Option D"],
                "correct_answer": "Correct answer or detailed explanation for non-multiple-choice questions.",
                "difficulty": "easy|medium|hard",
                "learning_objectives": ["objective1", "objective2"],
                "explanation": "A brief explanation of what concept this question is testing."
            }}
        ]
        """
        
        try:
            # Check if OpenAI API key is available
            if not os.getenv("OPENAI_API_KEY") or os.getenv("OPENAI_API_KEY") == "sk-your-***************here":
                print("OpenAI API key not configured, using fallback questions")
                return self._fallback_questions_with_history(submission, history)
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert programming instructor creating a quiz to test a student's true understanding of their code. Generate questions based on the provided code and analysis. Output JSON only."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.6,
                max_tokens=2500
            )
            
            # Parse AI response
            ai_response = response.choices[0].message.content
            print(f"AI Response: {ai_response}")  # Debug output
            
            # Check if response looks like an error message
            if ai_response.startswith("Internal") or ai_response.startswith("Error") or "error" in ai_response.lower():
                print(f"AI returned error message: {ai_response}")
                raise Exception(f"AI API Error: {ai_response}")
            
            questions = json.loads(ai_response)
            
            return questions
            
        except json.JSONDecodeError as e:
            print(f"JSON Parse Error: {str(e)}")
            print(f"Raw AI Response: {ai_response}")
            # Fallback to basic questions
            return self._fallback_questions_with_history(submission, history)
        except Exception as e:
            print(f"AI Generation Error: {str(e)}")  # Debug output
            # Fallback to basic questions
            return self._fallback_questions_with_history(submission, history)
    
    def _create_history_summary(self, history: List[Dict[str, Any]]) -> str:
        """Create a summary of submission history for quiz context"""
        if not history:
            return "No previous submissions available."
        
        summary = f"Previous {len(history)} submissions:\n"
        
        for i, sub in enumerate(history[:5]):  # Show last 5 submissions
            summary += f"- Submission {i+1}: {sub['assignment_name']} ({sub['file_name']}, {sub['file_size']} bytes)\n"
        
        return summary
    
    def _fallback_questions_with_history(self, submission: Submission, history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Fallback questions with historical context if AI generation fails"""
        
        # Generate questions based on actual code content
        code_lines = submission.file_content.split('\n')
        questions = []
        
        # Question 1: About the main function/entry point
        if 'def ' in submission.file_content:
            questions.append({
                "question_type": "code_explanation",
                "question_text": "What is the purpose of the main function in your code? Explain what it does when the program runs.",
                "code_snippet": "def calculator():\n    print(\"Simple Calculator\")",
                "options": [],
                "correct_answer": "explanation_required",
                "difficulty": "easy",
                "learning_objectives": ["function_understanding", "program_flow"],
                "explanation": "Tests understanding of the main program function"
            })
        
        # Question 2: About input handling
        if 'input(' in submission.file_content:
            questions.append({
                "question_type": "code_explanation",
                "question_text": "How does your program handle user input? What happens if a user enters invalid input?",
                "code_snippet": "choice = input(\"Enter choice (1-4): \")\nnum1 = float(input(\"Enter first number: \"))",
                "options": [],
                "correct_answer": "explanation_required",
                "difficulty": "medium",
                "learning_objectives": ["input_handling", "error_handling"],
                "explanation": "Tests understanding of input processing and validation"
            })
        
        # Question 3: About conditional logic
        if 'if ' in submission.file_content or 'elif ' in submission.file_content:
            questions.append({
                "question_type": "code_explanation",
                "question_text": "Explain the conditional logic in your code. What determines which operation is performed?",
                "code_snippet": "if choice == '1':\n    result = num1 + num2\nelif choice == '2':\n    result = num1 - num2",
                "options": [],
                "correct_answer": "explanation_required",
                "difficulty": "medium",
                "learning_objectives": ["conditional_logic", "control_flow"],
                "explanation": "Tests understanding of if/elif conditional statements"
            })
        
        # Question 4: About error handling
        if 'if ' in submission.file_content and '== 0' in submission.file_content:
            questions.append({
                "question_type": "code_explanation",
                "question_text": "What error handling did you implement in your code? Why was this necessary?",
                "code_snippet": "if num2 == 0:\n    print(\"Error: Cannot divide by zero!\")",
                "options": [],
                "correct_answer": "explanation_required",
                "difficulty": "medium",
                "learning_objectives": ["error_handling", "defensive_programming"],
                "explanation": "Tests understanding of error prevention and handling"
            })
        
        # Question 5: About code structure
        questions.append({
            "question_type": "code_explanation",
            "question_text": "How did you organize your code? What are the main components and how do they work together?",
            "code_snippet": f"File: {submission.file_name}\nLines: {len(code_lines)}",
            "options": [],
            "correct_answer": "explanation_required",
            "difficulty": "medium",
            "learning_objectives": ["code_organization", "program_structure"],
            "explanation": "Tests understanding of overall code structure and organization"
        })
        
        return questions
    
    def get_ai_analysis(self, submission_id: int, db: Session) -> Analysis:
        """Get AI analysis for a specific submission"""
        analysis = db.query(Analysis).filter(
            Analysis.submission_id == submission_id,
            Analysis.analysis_type == 'ai_enhanced_with_history'
        ).first()
        
        return analysis 

async def generate_quiz_questions(code_content: str, assignment_name: str) -> List[Dict[str, str]]:
    """
    Generate quiz questions using AI analysis of the code
    """
    try:
        # Try with a real API approach - mock the AI response for now until we get a real key
        api_key = os.getenv('OPENAI_API_KEY', 'sk-your-api-key-here')
        print(f"Debug: Using API key: {api_key[:10]}...")
        
        # For now, create intelligent questions based on code analysis instead of failing
        if api_key == 'sk-your-api-key-here':
            print("Debug: No real API key, creating intelligent code-based questions...")
            return create_intelligent_questions(code_content, assignment_name)
        
        # Only create client if we have a real API key
        client = get_client_or_none()
        if not client:
            print("Debug: No OpenAI client available, using intelligent questions...")
            return create_intelligent_questions(code_content, assignment_name)
        
        # Create a much more specific and detailed prompt
        prompt = f"""
You are an expert programming instructor creating quiz questions to verify that beginner Python students actually wrote and understand their {assignment_name} code submissions.

Analyze the provided code samples to understand what this {assignment_name} assignment involves, then create 5 STANDARDIZED questions that can test ANY student's comprehension of their own {assignment_name} implementation.

CODE SAMPLES TO ANALYZE:
{code_content}

CRITICAL REQUIREMENTS:
1. Create questions that work for ANY student's implementation of this {assignment_name} assignment
2. Focus on COMPREHENSION and APPLICATION - not memorization
3. Test understanding of design choices, problem-solving approach, and implementation decisions
4. Questions should prove the student wrote and understands their own code
5. Make questions appropriate for beginner Python programmers

QUESTION TYPES TO CREATE:
- Why did you choose [common technique] for [common problem in this assignment]?
- What would happen if you changed [common implementation choice] to [alternative]?
- How would you modify your code to [extend functionality relevant to assignment]?
- Explain the reasoning behind [design decision common to this assignment type]?
- What problem does [key component of this assignment] solve and why is it necessary?

GENERATE 5 STANDARDIZED QUESTIONS in this exact JSON format:
[
    {{
        "question": "Question that works for any student's implementation of {assignment_name}",
        "code_snippet": "General code concept or 'Your implementation'",
        "focus": "Comprehension/Application focus"
    }}
]

EXAMPLES FOR DIFFERENT ASSIGNMENT TYPES:
Voting System: "Why did you choose to validate voter IDs before allowing voting, and what would happen if you removed this validation?"
Calculator: "Explain why you chose to handle division by zero as a special case, and how would you modify your code to handle negative numbers differently?"
Banking System: "Why did you implement account balance checks before withdrawals, and how would you extend your code to support multiple account types?"

FOCUS ON: Universal concepts for this assignment type, design reasoning, modification scenarios
AVOID: Specific function names, exact code syntax, memorization questions
CREATE: Questions any student with this assignment can answer regardless of their specific implementation
"""

        print("Debug: Making AI request...")
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert programming instructor who creates precise, code-specific quiz questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        print("Debug: AI request completed successfully")

        content = response.choices[0].message.content.strip()
        print(f"AI Response received: {content[:200]}...")  # Debug: show first 200 chars
        
        # Handle potential error messages in response
        if "error" in content.lower() or "invalid" in content.lower():
            print(f"AI Generation Error: {content}")
            return generate_fallback_questions(code_content, assignment_name)
        
        # Try to parse JSON response
        try:
            questions_data = json.loads(content)
            if isinstance(questions_data, list) and len(questions_data) > 0:
                questions = []
                for i, q in enumerate(questions_data[:5], 1):  # Limit to 5 questions
                    questions.append({
                        "question": q.get("question", f"Question {i}"),
                        "code_snippet": q.get("code_snippet", ""),
                        "focus": q.get("focus", "")
                    })
                return questions
            else:
                raise ValueError("Invalid response format")
        except (json.JSONDecodeError, ValueError) as e:
            print(f"JSON parsing error: {e}")
            print(f"Raw response: {content}")
            return generate_fallback_questions(code_content, assignment_name)
            
    except Exception as e:
        print(f"AI Generation Error: {e}")
        print("Falling back to AI-generated questions with default API key...")
        # Try one more time with a more robust approach
        try:
            # Check if client exists (we might not have a real API key)
            if 'client' not in locals():
                print("Debug: No OpenAI client available, using intelligent questions...")
                return create_intelligent_questions(code_content, assignment_name)
            
            # Use a simpler prompt that's more likely to work
            simple_prompt = f"""
Generate 5 specific quiz questions about this {assignment_name} code:

{code_content}

Focus on:
1. Specific functions and their implementation
2. Database operations and data handling
3. User interface components and flow
4. Error handling and validation
5. Overall program logic and workflow

Return as JSON array with: question, code_snippet, focus
"""
            
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are a programming instructor. Generate specific quiz questions about the provided code."},
                    {"role": "user", "content": simple_prompt}
                ],
                temperature=0.1,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            print(f"Retry AI Response: {content[:200]}...")
            
            questions_data = json.loads(content)
            if isinstance(questions_data, list) and len(questions_data) > 0:
                questions = []
                for i, q in enumerate(questions_data[:5], 1):
                    questions.append({
                        "question": q.get("question", f"Question {i}"),
                        "code_snippet": q.get("code_snippet", ""),
                        "focus": q.get("focus", "")
                    })
                return questions
            else:
                raise ValueError("Invalid retry response format")
                
        except Exception as retry_error:
            print(f"Retry also failed: {retry_error}")
            raise Exception(f"AI quiz generation failed completely: {str(retry_error)}") 

def create_intelligent_questions(code_content: str, assignment_name: str) -> List[Dict[str, str]]:
    """
    Create intelligent comprehension questions based on actual code analysis
    """
    # Analyze the code to understand what it actually does
    lines = code_content.split('\n')
    functions = []
    classes = []
    imports = []
    db_operations = []
    ui_elements = []
    validation_checks = []
    
    for line in lines:
        line = line.strip()
        if line.startswith('def '):
            functions.append(line)
        elif line.startswith('class '):
            classes.append(line)
        elif 'import' in line:
            imports.append(line)
        elif any(db_word in line.lower() for db_word in ['sqlite', 'cursor', 'execute', 'commit']):
            db_operations.append(line)
        elif any(ui_word in line.lower() for ui_word in ['tkinter', 'button', 'label', 'entry', 'window']):
            ui_elements.append(line)
        elif any(val_word in line.lower() for val_word in ['if', 'validate', 'check', 'verify']):
            validation_checks.append(line)
    
    questions = []
    
    # Question 1: Design choice reasoning - reference actual code
    if 'voting' in assignment_name.lower():
        # Find actual validation code in their implementation
        validation_code = []
        for line in lines:
            if any(word in line.lower() for word in ['if', 'check', 'validate', 'verify', 'voter']):
                validation_code.append(line.strip())
        
        code_snippet = "\n".join(validation_code[:3]) if validation_code else "Your voter validation code"
        questions.append({
            "question": "Why did you choose to validate voter eligibility before allowing them to vote, and what would happen to the election integrity if you removed this validation?",
            "code_snippet": code_snippet,
            "focus": "Security design decisions"
        })
    elif 'calculator' in assignment_name.lower():
        # Find actual error handling code
        error_code = []
        for line in lines:
            if any(word in line.lower() for word in ['if', 'except', 'error', 'zero', 'division']):
                error_code.append(line.strip())
        
        code_snippet = "\n".join(error_code[:3]) if error_code else "Your error handling code"
        questions.append({
            "question": "Why did you choose to handle division by zero as a special case, and how would your program behave if you removed this error checking?",
            "code_snippet": code_snippet,
            "focus": "Error handling design"
        })
    else:
        # Find actual validation code
        validation_code = []
        for line in lines:
            if any(word in line.lower() for word in ['if', 'check', 'validate', 'verify']):
                validation_code.append(line.strip())
        
        code_snippet = "\n".join(validation_code[:3]) if validation_code else "Your validation code"
        questions.append({
            "question": f"Why did you choose the specific data validation approach in your {assignment_name} program, and what problems would arise if you removed these checks?",
            "code_snippet": code_snippet,
            "focus": "Input validation design"
        })
    
    # Question 2: Database/storage reasoning - reference actual code
    if db_operations:
        # Show actual database operations from their code
        db_snippet = "\n".join(db_operations[:3])
        questions.append({
            "question": "Explain why you chose to use a database to store information rather than just keeping data in variables, and how would you modify your database structure to handle additional data requirements?",
            "code_snippet": db_snippet,
            "focus": "Data persistence design"
        })
    else:
        # Find data storage code
        storage_code = []
        for line in lines:
            if any(word in line.lower() for word in ['=', 'store', 'save', 'data', 'variable']):
                storage_code.append(line.strip())
        
        code_snippet = "\n".join(storage_code[:3]) if storage_code else "Your data storage code"
        questions.append({
            "question": f"Why did you choose your specific data storage approach in this {assignment_name} program, and how would you modify it to handle larger amounts of data?",
            "code_snippet": code_snippet,
            "focus": "Data management design"
        })
    
    # Question 3: User interface reasoning - reference actual code
    if ui_elements:
        # Show actual UI code from their implementation
        ui_snippet = "\n".join(ui_elements[:3])
        questions.append({
            "question": "Why did you choose the specific user interface layout and components you implemented, and how would you modify the interface to improve user experience?",
            "code_snippet": ui_snippet,
            "focus": "UI design decisions"
        })
    else:
        # Find user interaction code
        interaction_code = []
        for line in lines:
            if any(word in line.lower() for word in ['input', 'print', 'user', 'interact']):
                interaction_code.append(line.strip())
        
        code_snippet = "\n".join(interaction_code[:3]) if interaction_code else "Your user interaction code"
        questions.append({
            "question": f"Why did you choose your specific user interaction approach in this {assignment_name} program, and how would you improve it for better usability?",
            "code_snippet": code_snippet,
            "focus": "User experience design"
        })
    
    # Question 4: Algorithm/logic reasoning - reference actual code
    if functions:
        main_function = next((f for f in functions if any(keyword in f.lower() for keyword in ['main', 'run', 'start', 'process'])), functions[0])
        func_name = main_function.split('(')[0].replace('def ', '')
        
        # Find the actual function code
        func_code = []
        in_function = False
        for line in lines:
            if line.strip().startswith(f'def {func_name}'):
                in_function = True
                func_code.append(line.strip())
            elif in_function and line.strip().startswith('def '):
                break
            elif in_function:
                func_code.append(line.strip())
        
        code_snippet = "\n".join(func_code[:5]) if func_code else f"Your {func_name} function"
        questions.append({
            "question": f"Explain the reasoning behind the logic flow in your {func_name} function, and what would happen if you changed the order of operations?",
            "code_snippet": code_snippet,
            "focus": "Algorithm design and flow control"
        })
    else:
        # Find main program logic
        logic_code = []
        for line in lines:
            if any(word in line.lower() for word in ['if', 'for', 'while', 'return', 'print']):
                logic_code.append(line.strip())
        
        code_snippet = "\n".join(logic_code[:5]) if logic_code else "Your main program logic"
        questions.append({
            "question": f"Explain the reasoning behind your overall program logic in this {assignment_name}, and what would happen if you changed the sequence of key operations?",
            "code_snippet": code_snippet,
            "focus": "Algorithm design"
        })
    
    # Question 5: Extension and modification
    if 'voting' in assignment_name.lower():
        questions.append({
            "question": "How would you modify your voting system to support multiple elections running simultaneously, and what changes would you need to make to your current code structure?",
            "code_snippet": "Current election handling",
            "focus": "Code extensibility and scalability"
        })
    elif 'calculator' in assignment_name.lower():
        questions.append({
            "question": "How would you extend your calculator to support advanced mathematical functions like trigonometry, and what modifications would you need to make to your current design?",
            "code_snippet": "Current calculation logic",
            "focus": "Feature extension design"
        })
    else:
        questions.append({
            "question": f"How would you extend your {assignment_name} program to handle more complex requirements, and what aspects of your current code design would need to change?",
            "code_snippet": "Current program structure",
            "focus": "Code extensibility and modification"
        })
    
    return questions 