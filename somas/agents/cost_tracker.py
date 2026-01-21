"""
Cost Tracker for GitHub Copilot Pro Plus

Tracks model usage and effectiveness for SOMAS autonomous pipeline.
No premium limits to manage - focus on effectiveness and optimization.

@copilot-context: Track usage patterns for fixed $10/month subscription
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class ModelUsageEntry:
    """Single usage record"""
    timestamp: str
    model: str
    request_type: str  # specification, simulation, implementation, etc.
    tokens_input: int
    tokens_output: int
    project_id: str
    duration_seconds: float
    success: bool
    error_message: Optional[str] = None


class CopilotCostTracker:
    """
    Tracks model usage patterns for Copilot Pro Plus.
    No premium limits to manage - focus on effectiveness.
    """
    
    def __init__(self, storage_path: str = ".somas/analytics/usage/"):
        """
        Initialize cost tracker
        
        Args:
            storage_path: Directory to store usage logs
        """
        self.storage_path = storage_path
        self.current_month_usage: Dict[str, List[ModelUsageEntry]] = {}
        self.monthly_cost = 10.00  # Fixed Copilot Pro Plus subscription
        
    def track_request(
        self,
        model: str,
        request_type: str,
        tokens_input: int,
        tokens_output: int,
        project_id: str,
        duration_seconds: float,
        success: bool,
        error_message: Optional[str] = None
    ) -> None:
        """Track a model usage request"""
        entry = ModelUsageEntry(
            timestamp=datetime.utcnow().isoformat(),
            model=model,
            request_type=request_type,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            project_id=project_id,
            duration_seconds=duration_seconds,
            success=success,
            error_message=error_message
        )
        
        # Add to current month tracking
        if model not in self.current_month_usage:
            self.current_month_usage[model] = []
        
        self.current_month_usage[model].append(entry)
        
        logger.info(
            f"Tracked {model} usage: {request_type} "
            f"({tokens_input + tokens_output} tokens, "
            f"{duration_seconds:.2f}s, "
            f"{'success' if success else 'failed'})"
        )
    
    def generate_usage_report(self) -> Dict[str, Any]:
        """Generate comprehensive usage report"""
        report = {
            'month': datetime.utcnow().strftime('%Y-%m'),
            'subscription': 'GitHub Copilot Pro Plus',
            'fixed_cost_usd': self.monthly_cost,
            'usage': {},
            'recommendations': []
        }
        
        for model in self.current_month_usage.keys():
            entries = self.current_month_usage[model]
            successful = sum(1 for e in entries if e.success)
            
            report['usage'][model] = {
                'total_requests': len(entries),
                'success_rate': f"{successful / len(entries):.2%}" if entries else "0%",
                'total_tokens': sum(e.tokens_input + e.tokens_output for e in entries)
            }
        
        return report
