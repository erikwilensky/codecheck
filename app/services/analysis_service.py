from typing import Dict, Any, List
from sqlalchemy.orm import Session
from ..models import Submission, Analysis, Student
from datetime import datetime
import re

class AnalysisService:
    def __init__(self):
        pass
    
    def analyze_submission(self, submission: Submission, db: Session) -> Analysis:
        """Perform basic analysis on a submission"""
        
        # Basic metrics analysis
        analysis_results = self._calculate_basic_metrics(submission)
        
        # Add tool dependency detection (Week 2 feature)
        tool_analysis = self._detect_tool_dependency(submission)
        analysis_results.update(tool_analysis)
        
        # Add learning progression analysis (Week 2 feature)
        progression_analysis = self._analyze_learning_progression(submission.student_id, db)
        analysis_results.update(progression_analysis)
        
        # Create analysis record
        analysis = Analysis(
            student_id=submission.student_id,
            submission_id=submission.id,
            analysis_type='enhanced',  # Updated to reflect Week 2 features
            status='completed',
            results=analysis_results,
            confidence_score=self._calculate_confidence_score(analysis_results),
            completed_at=datetime.utcnow()
        )
        
        db.add(analysis)
        db.commit()
        db.refresh(analysis)
        
        return analysis
    
    def _calculate_basic_metrics(self, submission: Submission) -> Dict[str, Any]:
        """Calculate basic metrics from submission"""
        
        metrics = {
            'files_changed': len(submission.files_changed) if submission.files_changed else 0,
            'lines_added': submission.lines_added,
            'lines_deleted': submission.lines_deleted,
            'net_lines': submission.lines_added - submission.lines_deleted,
            'commit_message_length': len(submission.commit_message),
            'has_meaningful_message': self._has_meaningful_commit_message(submission.commit_message),
            'file_types': self._analyze_file_types(submission.files_changed),
            'complexity_indicators': self._analyze_complexity_indicators(submission)
        }
        
        return metrics
    
    def _detect_tool_dependency(self, submission: Submission) -> Dict[str, Any]:
        """Detect potential tool dependency patterns (Week 2 feature)"""
        
        tool_indicators = {
            'ai_generation_probability': 0.0,
            'copilot_usage_probability': 0.0,
            'copy_paste_probability': 0.0,
            'knowledge_consistency_score': 0.0,
            'tool_dependency_risk': 'low'
        }
        
        # Analyze commit message for AI patterns
        if submission.commit_message:
            ai_message_score = self._analyze_commit_message_for_ai(submission.commit_message)
            tool_indicators['ai_generation_probability'] = ai_message_score
        
        # Analyze code volume patterns
        volume_score = self._analyze_code_volume_patterns(submission)
        tool_indicators['copilot_usage_probability'] = volume_score
        
        # Analyze file organization patterns
        organization_score = self._analyze_file_organization(submission)
        tool_indicators['copy_paste_probability'] = organization_score
        
        # Calculate overall tool dependency risk
        total_score = (tool_indicators['ai_generation_probability'] + 
                      tool_indicators['copilot_usage_probability'] + 
                      tool_indicators['copy_paste_probability']) / 3
        
        if total_score > 0.7:
            tool_indicators['tool_dependency_risk'] = 'high'
        elif total_score > 0.4:
            tool_indicators['tool_dependency_risk'] = 'medium'
        else:
            tool_indicators['tool_dependency_risk'] = 'low'
        
        return tool_indicators
    
    def _analyze_commit_message_for_ai(self, message: str) -> float:
        """Analyze commit message for AI generation patterns"""
        if not message:
            return 0.0
        
        message_lower = message.lower()
        ai_indicators = [
            'implement', 'add', 'create', 'update', 'fix', 'refactor', 'improve',
            'enhance', 'optimize', 'resolve', 'address', 'handle', 'support'
        ]
        
        # Check for overly descriptive patterns
        descriptive_count = sum(1 for indicator in ai_indicators if indicator in message_lower)
        
        # Check for perfect grammar and structure
        perfect_structure = len(message.split()) > 5 and message.endswith('.')
        
        # Calculate AI probability
        ai_score = min(1.0, (descriptive_count * 0.2 + (1.0 if perfect_structure else 0.0) * 0.3))
        
        return ai_score
    
    def _analyze_code_volume_patterns(self, submission: Submission) -> float:
        """Analyze code volume for Copilot-like patterns"""
        
        # Copilot often generates large, consistent blocks
        if submission.lines_added > 50 and submission.lines_deleted < 10:
            return 0.6  # High probability of Copilot usage
        
        # Balanced changes suggest manual work
        if abs(submission.lines_added - submission.lines_deleted) < 5:
            return 0.2  # Low probability
        
        return 0.4  # Medium probability
    
    def _analyze_file_organization(self, submission: Submission) -> float:
        """Analyze file organization for copy-paste patterns"""
        
        if not submission.files_changed:
            return 0.0
        
        # Multiple unrelated files suggest copy-paste
        if len(submission.files_changed) > 3:
            return 0.5
        
        # Single file changes are usually manual
        if len(submission.files_changed) == 1:
            return 0.1
        
        return 0.3
    
    def _analyze_learning_progression(self, student_id: int, db: Session) -> Dict[str, Any]:
        """Analyze learning progression over time (Week 2 feature)"""
        
        # Get student's submission history
        submissions = db.query(Submission).filter(
            Submission.student_id == student_id
        ).order_by(Submission.created_at.desc()).limit(10).all()
        
        if len(submissions) < 2:
            return {
                'learning_progression_score': 0.0,
                'skill_development_rate': 0.0,
                'consistency_score': 0.0,
                'sudden_improvement_detected': False,
                'learning_anomalies': []
            }
        
        # Calculate progression metrics
        progression_metrics = {
            'learning_progression_score': self._calculate_learning_progression_score(submissions),
            'skill_development_rate': self._calculate_skill_development_rate(submissions),
            'consistency_score': self._calculate_consistency_score(submissions),
            'sudden_improvement_detected': self._detect_sudden_improvements(submissions),
            'learning_anomalies': self._detect_learning_anomalies(submissions)
        }
        
        return progression_metrics
    
    def _calculate_learning_progression_score(self, submissions: List[Submission]) -> float:
        """Calculate overall learning progression score"""
        
        if len(submissions) < 2:
            return 0.0
        
        # Analyze commit message quality progression
        message_scores = [self._has_meaningful_commit_message(sub.commit_message) for sub in submissions]
        message_progression = sum(message_scores) / len(message_scores)
        
        # Analyze code volume progression
        volume_scores = [sub.lines_added for sub in submissions]
        volume_consistency = 1.0 - (max(volume_scores) - min(volume_scores)) / max(volume_scores) if max(volume_scores) > 0 else 0.0
        
        return (message_progression + volume_consistency) / 2
    
    def _calculate_skill_development_rate(self, submissions: List[Submission]) -> float:
        """Calculate rate of skill development"""
        
        if len(submissions) < 3:
            return 0.0
        
        # Analyze improvement in commit quality over time
        recent_submissions = submissions[:3]
        older_submissions = submissions[-3:]
        
        recent_quality = sum(1 for sub in recent_submissions if self._has_meaningful_commit_message(sub.commit_message))
        older_quality = sum(1 for sub in older_submissions if self._has_meaningful_commit_message(sub.commit_message))
        
        improvement_rate = (recent_quality - older_quality) / 3
        return max(0.0, min(1.0, improvement_rate))
    
    def _calculate_consistency_score(self, submissions: List[Submission]) -> float:
        """Calculate consistency in coding patterns"""
        
        if len(submissions) < 2:
            return 0.0
        
        # Analyze consistency in commit message length
        message_lengths = [len(sub.commit_message) for sub in submissions]
        length_variance = max(message_lengths) - min(message_lengths)
        length_consistency = 1.0 - (length_variance / max(message_lengths)) if max(message_lengths) > 0 else 0.0
        
        # Analyze consistency in code volume
        volumes = [sub.lines_added for sub in submissions]
        volume_variance = max(volumes) - min(volumes)
        volume_consistency = 1.0 - (volume_variance / max(volumes)) if max(volumes) > 0 else 0.0
        
        return (length_consistency + volume_consistency) / 2
    
    def _detect_sudden_improvements(self, submissions: List[Submission]) -> bool:
        """Detect sudden improvements that might indicate tool usage"""
        
        if len(submissions) < 3:
            return False
        
        # Compare recent vs older submissions
        recent = submissions[0]
        older = submissions[-1]
        
        # Check for sudden improvement in commit message quality
        recent_quality = self._has_meaningful_commit_message(recent.commit_message)
        older_quality = self._has_meaningful_commit_message(older.commit_message)
        
        # Check for sudden increase in code volume
        volume_increase = recent.lines_added > older.lines_added * 2
        
        return recent_quality and not older_quality and volume_increase
    
    def _detect_learning_anomalies(self, submissions: List[Submission]) -> List[str]:
        """Detect anomalies in learning patterns"""
        
        anomalies = []
        
        for i, submission in enumerate(submissions):
            # Check for inconsistent patterns
            if i > 0:
                prev_submission = submissions[i-1]
                
                # Sudden change in commit message style
                prev_quality = self._has_meaningful_commit_message(prev_submission.commit_message)
                curr_quality = self._has_meaningful_commit_message(submission.commit_message)
                
                if prev_quality != curr_quality:
                    anomalies.append(f"Inconsistent commit message quality at submission {submission.id}")
                
                # Sudden change in code volume
                volume_change = abs(submission.lines_added - prev_submission.lines_added)
                if volume_change > 50:
                    anomalies.append(f"Unusual code volume change at submission {submission.id}")
        
        return anomalies
    
    def _calculate_confidence_score(self, analysis_results: Dict[str, Any]) -> float:
        """Calculate confidence score for the analysis"""
        
        # Base confidence on data quality
        confidence = 0.8  # Base confidence
        
        # Adjust based on tool dependency risk
        tool_risk = analysis_results.get('tool_dependency_risk', 'low')
        if tool_risk == 'high':
            confidence += 0.1
        elif tool_risk == 'medium':
            confidence += 0.05
        
        # Adjust based on learning progression
        progression_score = analysis_results.get('learning_progression_score', 0.0)
        confidence += progression_score * 0.1
        
        return min(1.0, confidence)
    
    def _has_meaningful_commit_message(self, message: str) -> bool:
        """Check if commit message is meaningful"""
        if not message:
            return False
        
        # Remove common meaningless messages
        meaningless_patterns = [
            r'^update$',
            r'^fix$',
            r'^wip$',
            r'^commit$',
            r'^save$',
            r'^test$'
        ]
        
        message_lower = message.lower().strip()
        for pattern in meaningless_patterns:
            if re.match(pattern, message_lower):
                return False
        
        # Check if message has reasonable length and content
        return len(message.strip()) > 5 and not message.strip().isdigit()
    
    def _analyze_file_types(self, files_changed: List[str]) -> Dict[str, int]:
        """Analyze file types in the submission"""
        file_types = {}
        
        if not files_changed:
            return file_types
        
        for file_path in files_changed:
            if '.' in file_path:
                extension = file_path.split('.')[-1].lower()
                file_types[extension] = file_types.get(extension, 0) + 1
            else:
                file_types['no_extension'] = file_types.get('no_extension', 0) + 1
        
        return file_types
    
    def _analyze_complexity_indicators(self, submission: Submission) -> Dict[str, Any]:
        """Analyze complexity indicators in the submission"""
        indicators = {
            'large_change': submission.lines_added > 100 or submission.lines_deleted > 100,
            'many_files': len(submission.files_changed) > 5 if submission.files_changed else False,
            'balanced_changes': abs(submission.lines_added - submission.lines_deleted) < 10,
            'significant_addition': submission.lines_added > 50,
            'significant_deletion': submission.lines_deleted > 50
        }
        
        return indicators
    
    def get_submission_analysis(self, submission_id: int, db: Session) -> Analysis:
        """Get analysis for a specific submission"""
        analysis = db.query(Analysis).filter(
            Analysis.submission_id == submission_id,
            Analysis.analysis_type == 'enhanced'
        ).first()
        
        return analysis
    
    def get_student_analyses(self, student_id: int, db: Session, limit: int = 20) -> List[Analysis]:
        """Get recent analyses for a student"""
        analyses = db.query(Analysis).filter(
            Analysis.student_id == student_id
        ).order_by(Analysis.created_at.desc()).limit(limit).all()
        
        return analyses 