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

from somas.apo.constants import (
    AMBIGUITY_BASE, AMBIGUITY_WORD_MULTIPLIER, MAX_SCORE,
    NOVELTY_BASE, NOVELTY_WORD_MULTIPLIER, DEPENDENCIES_BASE,
    DEPENDENCIES_WORD_MULTIPLIER, RISK_BASE, RISK_WORD_MULTIPLIER,
    RISK_CONTEXT_ADDITION, TECHNICAL_DEPTH_BASE,
    TECHNICAL_DEPTH_WORD_MULTIPLIER, DEFAULT_SECURITY_RISK_MULTIPLIER,
    DEFAULT_EXTERNAL_DEPENDENCY_MULTIPLIER,
    DEFAULT_NOVEL_TECHNOLOGY_MULTIPLIER, HIGH_RISK_THRESHOLD,
    AMBIGUOUS_WORDS, NOVEL_INDICATORS, DEPENDENCY_INDICATORS,
    HIGH_RISK_INDICATORS, SPECIALIZED_TERMS
)

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
            'moderate': 3.0,
            'complex': 5.0
        })
        
    def _default_config(self) -> Dict[str, Any]:
        """Default configuration if not provided"""
        return {
            'task_analyzer': {
                'minimum_complexity_for_apo': 2.0,
                'complexity_thresholds': {
                    'simple': 2.0,
                    'moderate': 3.0,
                    'complex': 5.0
                },
                'auto_routing': {
                    'enabled': True,
                    'rules': [
                        {'complexity': '> 3.0', 'model': 'claude_opus_4_5', 'chain': 'draft_critique_refine'},
                        {'complexity': '2.0-3.0', 'model': 'claude_sonnet_4_5', 'chain': 'sequential'},
                        {'complexity': '< 2.0', 'model': 'grok_code_fast_1', 'chain': 'sequential'}
                    ]
                },
                'risk_factors': {
                    'security_risk_multiplier': DEFAULT_SECURITY_RISK_MULTIPLIER,
                    'external_dependency_multiplier': DEFAULT_EXTERNAL_DEPENDENCY_MULTIPLIER,
                    'novel_technology_multiplier': DEFAULT_NOVEL_TECHNOLOGY_MULTIPLIER
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
        
        if advisor_agent:
            return self._analyze_with_advisor(task_description, context, advisor_agent)
        
        return self.__analyze_heuristic_task(task_description, context)
        
    def _analyze_with_advisor(
        self,
        task_description: str,
        context: Dict[str, Any],
        advisor_agent: Any,
    ) -> ComplexityAnalysis:
        """
        Perform complexity analysis using an optional advisor agent.

        The advisor can refine or override the heuristic analysis. If anything
        goes wrong while calling the advisor, we safely fall back to the
        heuristic result to avoid breaking task routing.
        """
        base_analysis = self.__analyze_heuristic_task(task_description, context)

        if advisor_agent is None:
            return base_analysis

        try:
            advisor_method = getattr(advisor_agent, "analyze_task", None)
            if callable(advisor_method):
                advisor_result = advisor_method(
                    task_description=task_description,
                    context=context,
                    base_analysis=base_analysis,
                )
            else:
                advisor_method = getattr(advisor_agent, "advise_on_complexity", None)
                if not callable(advisor_method):
                    return base_analysis
                advisor_result = advisor_method(
                    task_description=task_description,
                    context=context,
                    base_analysis=base_analysis,
                )

            if isinstance(advisor_result, ComplexityAnalysis):
                return advisor_result

            if isinstance(advisor_result, dict):
                merged = base_analysis.__dict__.copy()
                merged.update(advisor_result)
                try:
                    return ComplexityAnalysis(**merged)
                except TypeError:
                    logger.warning(
                        "Advisor returned incompatible dict structure; "
                        "falling back to heuristic analysis",
                    )
                    return base_analysis
        except Exception as exc:
            logger.warning(
                "Advisor-based analysis failed; falling back to heuristic "
                "analysis: %s",
                exc,
            )
        return base_analysis
    
    def __analyze_heuristic_task(
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
        dimensions = self.__calculate_dimensions(task_description, context)
        complexity_score = self.__calculate_complexity_score(dimensions, context)
        return self.__generate_analysis_from_score(complexity_score, dimensions)

    def __calculate_dimensions(self, task_description: str, context: Dict[str, Any]) -> Dict[str, float]:
        """Calculate the complexity dimensions."""
        return {
            'ambiguity': self._score_ambiguity(task_description),
            'novelty': self._score_novelty(task_description),
            'dependencies': self._score_dependencies(task_description),
            'risk': self._score_risk(task_description, context),
            'technical_depth': self._score_technical_depth(task_description)
        }

    def __calculate_complexity_score(self, dimensions: Dict[str, float], context: Dict[str, Any]) -> float:
        """Calculate the overall complexity score."""
        base_score = sum(dimensions.values()) / len(dimensions)
        return self._apply_risk_multipliers(base_score, context)

    def __generate_analysis_from_score(self, complexity_score: float, dimensions: Dict[str, float]) -> ComplexityAnalysis:
        """Generate the full analysis from the complexity score."""
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
            confidence=0.7,
            reasoning=f"Heuristic analysis: {complexity_level.value} complexity"
        )
    
    def _cap_score(self, score: float) -> float:
        """Cap the score at the maximum value."""
        return min(score, MAX_SCORE)

    def _score_ambiguity(self, task_description: str) -> float:
        """
        Score ambiguity based on language patterns
        
        Note: Simple keyword matching for POC. Production would use NLP analysis.
        Known limitation: Can match keywords in unrelated contexts (e.g., "new" in "renew").
        """
        count = sum(1 for word in AMBIGUOUS_WORDS if word in task_description.lower())
        score = AMBIGUITY_BASE + (count * AMBIGUITY_WORD_MULTIPLIER)
        return self._cap_score(score)
    
    def _score_novelty(self, task_description: str) -> float:
        """
        Score novelty based on technology and patterns
        
        Note: Simple keyword matching for POC. Production would use contextual analysis.
        Known limitation: Matches partial words (e.g., "new" in "renew subscription").
        """
        count = sum(1 for word in NOVEL_INDICATORS if word in task_description.lower())
        score = NOVELTY_BASE + (count * NOVELTY_WORD_MULTIPLIER)
        return self._cap_score(score)
    
    def _score_dependencies(self, task_description: str) -> float:
        """
        Score dependencies based on external mentions
        
        Note: Simple keyword matching for POC. Production would parse actual dependencies.
        """
        count = sum(1 for word in DEPENDENCY_INDICATORS if word in task_description.lower())
        score = DEPENDENCIES_BASE + (count * DEPENDENCIES_WORD_MULTIPLIER)
        return self._cap_score(score)
    
    def _score_risk(self, task_description: str, context: Dict[str, Any]) -> float:
        """
        Score risk based on impact indicators
        
        Note: Simple keyword matching for POC. Production would use risk modeling.
        Known limitation: Matches keywords in comments (e.g., "# security: this is safe").
        """
        count = sum(1 for word in HIGH_RISK_INDICATORS if word in task_description.lower())
        
        if context.get('security_sensitive', False):
            count += RISK_CONTEXT_ADDITION
            
        score = RISK_BASE + (count * RISK_WORD_MULTIPLIER)
        return self._cap_score(score)
    
    def _score_technical_depth(self, task_description: str) -> float:
        """
        Score technical depth based on specialized terms
        
        Note: Simple keyword matching for POC. Production would assess actual complexity.
        """
        count = sum(1 for word in SPECIALIZED_TERMS if word in task_description.lower())
        score = TECHNICAL_DEPTH_BASE + (count * TECHNICAL_DEPTH_WORD_MULTIPLIER)
        return self._cap_score(score)
    
    def _apply_risk_multipliers(self, score: float, context: Dict[str, Any]) -> float:
        """Apply risk multipliers from configuration"""
        risk_factors = self.config.get('task_analyzer', {}).get('risk_factors', {})
        
        if context.get('security_risk', False):
            score *= risk_factors.get('security_risk_multiplier', DEFAULT_SECURITY_RISK_MULTIPLIER)
        
        if context.get('external_dependency', False):
            score *= risk_factors.get('external_dependency_multiplier', DEFAULT_EXTERNAL_DEPENDENCY_MULTIPLIER)
        
        if context.get('novel_technology', False):
            score *= risk_factors.get('novel_technology_multiplier', DEFAULT_NOVEL_TECHNOLOGY_MULTIPLIER)
        
        return self._cap_score(score)
    
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
        
        if dimensions.get('risk', 0) > HIGH_RISK_THRESHOLD:
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
        default_model = 'claude_sonnet_4_5'
        
        for rule in rules:
            complexity_range = rule.get('complexity', '')
            model = rule.get('model', default_model)

            try:
                if '>' in complexity_range:
                    threshold = float(complexity_range.split('>')[1].strip())
                    if complexity_score > threshold:
                        return model
                
                elif '-' in complexity_range:
                    low, high = map(float, complexity_range.split('-'))
                    if low <= complexity_score < high:
                        return model
                
                elif '<' in complexity_range:
                    threshold = float(complexity_range.split('<')[1].strip())
                    if complexity_score < threshold:
                        return model
            except (ValueError, IndexError) as e:
                logger.warning(f"Could not parse complexity rule '{complexity_range}': {e}")
        return default_model

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
        logger.info(f"Loading configuration from {config_path}")
    
    return APOTaskAnalyzer(config)