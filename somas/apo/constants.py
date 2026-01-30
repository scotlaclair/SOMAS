"""Constants for the Task Complexity Analyzer."""

# Complexity Dimensions Weights
AMBIGUITY_BASE = 1.0
AMBIGUITY_WORD_MULTIPLIER = 0.6

NOVELTY_BASE = 2.5
NOVELTY_WORD_MULTIPLIER = 1.2

DEPENDENCIES_BASE = 1.5
DEPENDENCIES_WORD_MULTIPLIER = 1.0

RISK_BASE = 1.5
RISK_WORD_MULTIPLIER = 0.9
RISK_CONTEXT_ADDITION = 2.5

TECHNICAL_DEPTH_BASE = 2.5
TECHNICAL_DEPTH_WORD_MULTIPLIER = 0.8

# Scoring Caps
MAX_SCORE = 5.0

# Risk Multipliers
DEFAULT_SECURITY_RISK_MULTIPLIER = 2.5
DEFAULT_EXTERNAL_DEPENDENCY_MULTIPLIER = 1.5
DEFAULT_NOVEL_TECHNOLOGY_MULTIPLIER = 2.0

# Thresholds
HIGH_RISK_THRESHOLD = 3.5

# Keywords
AMBIGUOUS_WORDS = ['maybe', 'probably', 'might', 'could', 'should', 'etc', 'and so on']
NOVEL_INDICATORS = ['new', 'novel', 'first time', 'unprecedented', 'experimental']
DEPENDENCY_INDICATORS = ['api', 'service', 'external', 'integration', 'third-party']
HIGH_RISK_INDICATORS = ['security', 'authentication', 'payment', 'data loss', 'critical']
SPECIALIZED_TERMS = ['algorithm', 'optimization', 'cryptography', 'ml', 'ai', 'distributed']