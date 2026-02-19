"""
Question Set Version Management
Manages versioned question sets with Git integration
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json
import hashlib
import logging

logger = logging.getLogger(__name__)


@dataclass
class Question:
    """Individual question"""
    id: str
    text: str
    intent_type: str  # informational, transactional, comparison, local
    category: str
    language: str = "en"
    metadata: Dict = field(default_factory=dict)


@dataclass
class EvaluationConfig:
    """Evaluation configuration"""
    engines: List[str]
    temperature: float = 0.7
    max_tokens: int = 1000
    seed: Optional[int] = 42
    region: Optional[str] = None
    language: Optional[str] = "en"


@dataclass
class QuestionSet:
    """Versioned question set"""
    name: str
    version: str
    created_at: datetime
    questions: List[Question]
    evaluation_config: EvaluationConfig
    description: str = ""
    tags: List[str] = field(default_factory=list)
    commit_hash: Optional[str] = None


class QuestionSetManager:
    """Manage question set versions"""
    
    def __init__(self, storage_path: str = "./question_sets"):
        self.storage_path = storage_path
        self.question_sets: Dict[str, List[QuestionSet]] = {}
    
    def create_question_set(
        self,
        name: str,
        questions: List[Question],
        evaluation_config: EvaluationConfig,
        description: str = "",
        tags: List[str] = None
    ) -> QuestionSet:
        """Create a new question set version"""
        try:
            # Generate version number
            version = self._generate_version(name)
            
            # Create question set
            question_set = QuestionSet(
                name=name,
                version=version,
                created_at=datetime.now(),
                questions=questions,
                evaluation_config=evaluation_config,
                description=description,
                tags=tags or []
            )
            
            # Save to storage
            self._save_question_set(question_set)
            
            # Commit to Git (if available)
            commit_hash = self._commit_to_git(question_set)
            question_set.commit_hash = commit_hash
            
            # Add to in-memory storage
            if name not in self.question_sets:
                self.question_sets[name] = []
            self.question_sets[name].append(question_set)
            
            logger.info(f"Created question set: {name} v{version}")
            return question_set
            
        except Exception as e:
            logger.error(f"Failed to create question set: {e}")
            raise
    
    def get_question_set(self, name: str, version: Optional[str] = None) -> Optional[QuestionSet]:
        """Get question set by name and version"""
        if name not in self.question_sets:
            return None
        
        versions = self.question_sets[name]
        
        if version is None:
            # Return latest version
            return versions[-1] if versions else None
        
        # Find specific version
        for qs in versions:
            if qs.version == version:
                return qs
        
        return None
    
    def list_versions(self, name: str) -> List[str]:
        """List all versions of a question set"""
        if name not in self.question_sets:
            return []
        
        return [qs.version for qs in self.question_sets[name]]
    
    def compare_versions(self, name: str, version1: str, version2: str) -> Dict:
        """Compare two versions of a question set"""
        qs1 = self.get_question_set(name, version1)
        qs2 = self.get_question_set(name, version2)
        
        if not qs1 or not qs2:
            raise ValueError("One or both versions not found")
        
        # Compare questions
        q1_ids = {q.id for q in qs1.questions}
        q2_ids = {q.id for q in qs2.questions}
        
        added = q2_ids - q1_ids
        removed = q1_ids - q2_ids
        common = q1_ids & q2_ids
        
        # Check for modified questions
        modified = []
        for qid in common:
            q1 = next(q for q in qs1.questions if q.id == qid)
            q2 = next(q for q in qs2.questions if q.id == qid)
            if q1.text != q2.text or q1.intent_type != q2.intent_type:
                modified.append(qid)
        
        # Compare evaluation config
        config_changed = (
            qs1.evaluation_config.engines != qs2.evaluation_config.engines or
            qs1.evaluation_config.temperature != qs2.evaluation_config.temperature or
            qs1.evaluation_config.max_tokens != qs2.evaluation_config.max_tokens
        )
        
        return {
            "name": name,
            "version1": version1,
            "version2": version2,
            "questions": {
                "added": list(added),
                "removed": list(removed),
                "modified": modified,
                "total_v1": len(qs1.questions),
                "total_v2": len(qs2.questions)
            },
            "evaluation_config_changed": config_changed,
            "config_diff": {
                "engines": {
                    "v1": qs1.evaluation_config.engines,
                    "v2": qs2.evaluation_config.engines
                }
            } if config_changed else None
        }
    
    def _generate_version(self, name: str) -> str:
        """Generate next version number"""
        if name not in self.question_sets or not self.question_sets[name]:
            return "1.0.0"
        
        latest = self.question_sets[name][-1]
        major, minor, patch = map(int, latest.version.split('.'))
        
        # Increment minor version
        return f"{major}.{minor + 1}.{patch}"
    
    def _save_question_set(self, question_set: QuestionSet):
        """Save question set to storage"""
        # Mock implementation - in production, save to file system or database
        logger.info(f"Saving question set: {question_set.name} v{question_set.version}")
    
    def _commit_to_git(self, question_set: QuestionSet) -> Optional[str]:
        """Commit question set to Git"""
        try:
            # Mock implementation - in production, use GitPython
            # Generate mock commit hash
            content = json.dumps({
                "name": question_set.name,
                "version": question_set.version,
                "questions": len(question_set.questions)
            })
            commit_hash = hashlib.sha1(content.encode()).hexdigest()[:8]
            
            logger.info(f"Committed to Git: {commit_hash}")
            return commit_hash
            
        except Exception as e:
            logger.warning(f"Git commit failed: {e}")
            return None


class BenchmarkQuestionSets:
    """Pre-defined benchmark question sets"""
    
    @staticmethod
    def create_ecommerce_benchmark() -> List[Question]:
        """Create e-commerce benchmark questions"""
        return [
            Question(
                id="ecom_001",
                text="What are the best wireless headphones under $200?",
                intent_type="comparison",
                category="electronics"
            ),
            Question(
                id="ecom_002",
                text="Where can I buy organic coffee beans online?",
                intent_type="transactional",
                category="food"
            ),
            Question(
                id="ecom_003",
                text="How do I choose the right running shoes?",
                intent_type="informational",
                category="sports"
            ),
            Question(
                id="ecom_004",
                text="Best laptop for programming in 2026",
                intent_type="comparison",
                category="electronics"
            ),
            Question(
                id="ecom_005",
                text="What is the return policy for online purchases?",
                intent_type="informational",
                category="policy"
            ),
        ]
    
    @staticmethod
    def create_local_business_benchmark() -> List[Question]:
        """Create local business benchmark questions"""
        return [
            Question(
                id="local_001",
                text="Best Italian restaurant near me",
                intent_type="local",
                category="restaurant"
            ),
            Question(
                id="local_002",
                text="Dentist open on weekends in downtown",
                intent_type="local",
                category="healthcare"
            ),
            Question(
                id="local_003",
                text="Where to get car oil change nearby",
                intent_type="local",
                category="automotive"
            ),
            Question(
                id="local_004",
                text="24 hour pharmacy in my area",
                intent_type="local",
                category="pharmacy"
            ),
            Question(
                id="local_005",
                text="Best coffee shop for working remotely",
                intent_type="local",
                category="cafe"
            ),
        ]
    
    @staticmethod
    def create_saas_benchmark() -> List[Question]:
        """Create SaaS benchmark questions"""
        return [
            Question(
                id="saas_001",
                text="What is the best project management tool for small teams?",
                intent_type="comparison",
                category="productivity"
            ),
            Question(
                id="saas_002",
                text="How to integrate CRM with email marketing?",
                intent_type="informational",
                category="integration"
            ),
            Question(
                id="saas_003",
                text="Pricing comparison: Salesforce vs HubSpot",
                intent_type="comparison",
                category="crm"
            ),
            Question(
                id="saas_004",
                text="What features should I look for in accounting software?",
                intent_type="informational",
                category="finance"
            ),
            Question(
                id="saas_005",
                text="Best video conferencing tool for remote teams",
                intent_type="comparison",
                category="communication"
            ),
        ]


# Global question set manager instance
question_set_manager = QuestionSetManager()
