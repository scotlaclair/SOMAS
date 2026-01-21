"""
APO Task Complexity Analyzer

Analyzes task complexity on multiple dimensions and routes to appropriate
mental models and chain strategies based on complexity scores.

@copilot-context: Critical for autonomous task routing
"""

import logging
from typing import Dict, Any, Optional, List
from enum import Enum
from dataclasses import dataclass

logger = logging.getLogger(__name__)


class ComplexityLevel(Enum):
    """Task complexity levels"""
    SIMPLE = "simple"           # < 2.0 - Straightforward, low risk
    MODERATE = "moderate"       # 2.0-3.5 - Some complexity, manageable risk
    COMPLEX = "complex"         # > 3.5 - High complexity, significant risk


class MentalModel(Enum):
    """Available mental models from APO"""
    FIRST_PRINCIPLES = "first_principles"
    INVERSION = "inversion"
    SECOND_ORDER_THINKING = "second_order_thinking"
    OODA_LOOP = "ooda_loop"
    OCCAMS_RAZOR = "occams_razor"
    SIX_THINKING_HATS = "six_thinking_hats"
    TREE_OF_THOUGHTS = "tree_of_thoughts"


class ChainStrategy(Enum):
    """Available chain strategies from APO"""
    SEQUENTIAL = "sequential"
    COLLISION = "collision"
    DRAFT_CRITIQUE_REFINE = "draft_critique_refine"
    PARALLEL_SYNTHESIS = "parallel_synthesis"
    STRATEGIC_DIAMOND = "strategic_diamond"


@dataclass
class ComplexityAnalysis:
    """Result of task complexity analysis"""
    complexity_score: float
    complexity_level: ComplexityLevel
    dimensions: Dict[str, float]
    recommended_mental_model: List[MentalModel]
    recommended_chain_strategy: ChainStrategy
    recommended_model: str
    confidence: float
    reasoning: str


class APOTaskAnalyzer:
    """
    Analyzes task complexity and recommends appropriate strategies.
    
    Evaluates tasks on 5 dimensions:
    1. Ambiguity: How unclear are requirements?
    2. Novelty: How unprecedented is this?
    3. Dependencies: How many external factors?
    4. Risk: Cost of failure?
    5. Technical Depth: How specialized is knowledge?
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize task analyzer
        
        Args:
            config: APO configuration from .somas/config.yml
        """
        self.config = config or self._default_config()
        self.thresholds = self.config.get('task_analyzer', {}).get('complexity_thresholds', {
            'simple': 2.0,
            'moderate': 3.5,
            'complex': 5.0
        })
        
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration if not provided"""
        return {
            'task_analyzer': {
                'minimum_complexity_for_apo': 2.0,
                'complexity_thresholds': {
                    'simple': 2.0,
                    'moderate': 3.5,
                    'complex': 5.0
                },
                'auto_routing': {
                    'enabled': True,
                    'rules': [
                        {'complexity': '> 3.5', 'model': 'claude_opus_4_5', 'chain': 'draft_critique_refine'},
                        {'complexity': '2.0-3.5', 'model': 'claude_sonnet_4_5', 'chain': 'sequential'},
                        {'complexity': '< 2.0', 'model': 'grok_code_fast_1', 'chain': 'sequential'}
                    ]
                }
            }
        }
    
    def analyze_task(
        self,
        task_description: str,
        context: Optional[Dict[str, Any]] = None,
        advisor_agent: Optional[Any] = None
    ) -> ComplexityAnalysis:
        """
        Analyze task complexity on multiple dimensions
        
        Args:
            task_description: Description of the task
            context: Additional context about the task
            advisor_agent: Optional advisor agent for advanced analysis
            
        Returns:
            ComplexityAnalysis with scores and recommendations
        """
        context = context or {}
        
        # If advisor agent available, use it for sophisticated analysis
        if advisor_agent:
            return self._analyze_with_advisor(task_description, context, advisor_agent)
        
        # Otherwise, use heuristic-based analysis
        return self._analyze_heuristic(task_description, context)
    
    def _analyze_with_advisor(
        self,
        task_description: str,
        context: Dict[str, Any],
        advisor_agent: Any
    ) -> ComplexityAnalysis:
        """
        Perform complexity analysis using advisor agent
        
        Note: This is a placeholder for POC. Production would call actual advisor.
        Falls back to heuristic analysis if advisor fails.
        
        Args:
            task_description: Task to analyze
            context: Additional context
            advisor_agent: Advisor agent instance (placeholder in POC)
            
        Returns:
            ComplexityAnalysis from advisor or heuristic fallback
        """
        # TODO: Implement actual advisor agent integration
        # For POC, fall back to heuristic analysis
        logger.info("Advisor agent integration not yet implemented, using heuristics")
        return self._analyze_heuristic(task_description, context)
    
    def _analyze_heuristic(
        self,
        task_description: str,
        context: Dict[str, Any]
    ) -> ComplexityAnalysis:
        """
        Heuristic-based complexity analysis
        
        Args:
            task_description: Task to analyze
            context: Additional context
            
        Returns:
            ComplexityAnalysis based on heuristics
        """
        # Analyze each dimension using heuristics
        dimensions = {
            'ambiguity': self._score_ambiguity(task_description),
            'novelty': self._score_novelty(task_description, context),
            'dependencies': self._score_dependencies(task_description, context),
            'risk': self._score_risk(task_description, context),
            'technical_depth': self._score_technical_depth(task_description, context)
        }
        
        # Calculate overall complexity
        complexity_score = sum(dimensions.values()) / len(dimensions)
        
        # Apply risk multipliers
        complexity_score = self._apply_risk_multipliers(complexity_score, context)
        
        # Determine recommendations
        complexity_level = self._determine_complexity_level(complexity_score)
        mental_models = self._select_mental_models(complexity_level, dimensions)
        chain_strategy = self._select_chain_strategy(complexity_level)
        recommended_model = self._route_to_model(complexity_score)
        
        return ComplexityAnalysis(
            complexity_score=complexity_score,
            complexity_level=complexity_level,
            dimensions=dimensions,
            recommended_mental_model=mental_models,
            recommended_chain_strategy=chain_strategy,
            recommended_model=recommended_model,
            confidence=0.7,  # Heuristic analysis is less confident
            reasoning=f"Heuristic analysis: {complexity_level.value} complexity"
        )
    
    def _score_ambiguity(self, task_description: str) -> float:
        """
        Score ambiguity based on language patterns
        
        Note: Simple keyword matching for POC. Production would use NLP analysis.
        Known limitation: Can match keywords in unrelated contexts (e.g., "new" in "renew").
        """
        ambiguous_words = ['maybe', 'probably', 'might', 'could', 'should', 'etc', 'and so on']
        count = sum(1 for word in ambiguous_words if word in task_description.lower())
        return min(5.0, 1.0 + (count * 0.5))
    
    def _score_novelty(self, task_description: str, context: Dict[str, Any]) -> float:
        """
        Score novelty based on technology and patterns
        
        Note: Simple keyword matching for POC. Production would use contextual analysis.
        Known limitation: Matches partial words (e.g., "new" in "renew subscription").
        """
        novel_indicators = ['new', 'novel', 'first time', 'unprecedented', 'experimental']
        count = sum(1 for word in novel_indicators if word in task_description.lower())
        return min(5.0, 2.0 + count)
    
    def _score_dependencies(self, task_description: str, context: Dict[str, Any]) -> float:
        """
        Score dependencies based on external mentions
        
        Note: Simple keyword matching for POC. Production would parse actual dependencies.
        """
        dependency_indicators = ['api', 'service', 'external', 'integration', 'third-party']
        count = sum(1 for word in dependency_indicators if word in task_description.lower())
        return min(5.0, 1.0 + (count * 0.8))
    
    def _score_risk(self, task_description: str, context: Dict[str, Any]) -> float:
        """
        Score risk based on impact indicators
        
        Note: Simple keyword matching for POC. Production would use risk modeling.
        Known limitation: Matches keywords in comments (e.g., "# security: this is safe").
        """
        high_risk_indicators = ['security', 'authentication', 'payment', 'data loss', 'critical']
        count = sum(1 for word in high_risk_indicators if word in task_description.lower())
        
        # Check context for security flag
        if context.get('security_sensitive', False):
            count += 2
            
        return min(5.0, 1.0 + (count * 0.7))
    
    def _score_technical_depth(self, task_description: str, context: Dict[str, Any]) -> float:
        """
        Score technical depth based on specialized terms
        
        Note: Simple keyword matching for POC. Production would assess actual complexity.
        """
        specialized_terms = ['algorithm', 'optimization', 'cryptography', 'ml', 'ai', 'distributed']
        count = sum(1 for word in specialized_terms if word in task_description.lower())
        return min(5.0, 2.0 + (count * 0.6))
    
    def _apply_risk_multipliers(self, score: float, context: Dict[str, Any]) -> float:
        """Apply risk multipliers from configuration"""
        risk_factors = self.config.get('task_analyzer', {}).get('risk_factors', {})
        
        if context.get('security_risk', False):
            score *= risk_factors.get('security_risk_multiplier', 2.5)
        
        if context.get('external_dependency', False):
            score *= risk_factors.get('external_dependency_multiplier', 1.5)
        
        if context.get('novel_technology', False):
            score *= risk_factors.get('novel_technology_multiplier', 2.0)
        
        return min(5.0, score)  # Cap at 5.0
    
    def _determine_complexity_level(self, score: float) -> ComplexityLevel:
        """Determine complexity level from score"""
        if score < self.thresholds['simple']:
            return ComplexityLevel.SIMPLE
        elif score < self.thresholds['moderate']:
            return ComplexityLevel.MODERATE
        else:
            return ComplexityLevel.COMPLEX
    
    def _select_mental_models(
        self,
        complexity_level: ComplexityLevel,
        dimensions: Dict[str, float]
    ) -> List[MentalModel]:
        """Select appropriate mental models"""
        models = []
        
        if complexity_level == ComplexityLevel.SIMPLE:
            models = [MentalModel.OCCAMS_RAZOR]
        elif complexity_level == ComplexityLevel.MODERATE:
            models = [MentalModel.OODA_LOOP, MentalModel.SECOND_ORDER_THINKING]
        else:
            models = [MentalModel.FIRST_PRINCIPLES, MentalModel.TREE_OF_THOUGHTS]
        
        # Add inversion for high-risk tasks
        if dimensions.get('risk', 0) > 3.5:
            models.append(MentalModel.INVERSION)
        
        return models
    
    def _select_chain_strategy(self, complexity_level: ComplexityLevel) -> ChainStrategy:
        """Select appropriate chain strategy"""
        if complexity_level == ComplexityLevel.SIMPLE:
            return ChainStrategy.SEQUENTIAL
        elif complexity_level == ComplexityLevel.MODERATE:
            return ChainStrategy.SEQUENTIAL
        else:
            return ChainStrategy.DRAFT_CRITIQUE_REFINE
    
    def _route_to_model(self, complexity_score: float) -> str:
        """Route to appropriate AI model based on complexity"""
        rules = self.config.get('task_analyzer', {}).get('auto_routing', {}).get('rules', [])
        
        for rule in rules:
            complexity_range = rule.get('complexity', '')
            
            if '>' in complexity_range:
                threshold = float(complexity_range.split('>')[1].strip())
                if complexity_score > threshold:
                    return rule.get('model', 'claude_sonnet_4_5')
            
            elif '-' in complexity_range:
                low, high = map(float, complexity_range.split('-'))
                if low <= complexity_score < high:
                    return rule.get('model', 'claude_sonnet_4_5')
            
            elif '<' in complexity_range:
                threshold = float(complexity_range.split('<')[1].strip())
                if complexity_score < threshold:
                    return rule.get('model', 'grok_code_fast_1')
        
        # Default to Claude Sonnet 4.5
        return 'claude_sonnet_4_5'


def create_analyzer(config_path: Optional[str] = None) -> APOTaskAnalyzer:
    """
    Factory function to create task analyzer
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configured APOTaskAnalyzer instance
    """
    config = None
    if config_path:
        # In production, load from YAML file
        logger.info(f"Loading configuration from {config_path}")
    
    return APOTaskAnalyzer(config)
