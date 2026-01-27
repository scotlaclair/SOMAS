"""
Circuit breaker infrastructure for SOMAS autonomous pipeline.
Prevents infinite loops, comment explosions, and runaway automation.
"""

import re
import yaml
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional


class CircuitBreaker:
    """Safeguards for autonomous pipeline operations."""
    
    # Marker patterns for idempotency
    MARKERS = {
        'initialized': '<!-- SOMAS_INITIALIZED -->',
        'pr_continue': '<!-- SOMAS_PR_CONTINUE:PR-{pr_number} -->',
        'recommendations_captured': '<!-- SOMAS_RECOMMENDATIONS_CAPTURED:{count} -->',
        'stage_complete': '<!-- SOMAS_STAGE_COMPLETE:{stage} -->',
        'circuit_breaker': '<!-- SOMAS_CIRCUIT_BREAKER:{reason} -->',
    }
    
    def __init__(self, config_path: str = ".somas/config/limits.yml"):
        self.config = self._load_config(config_path)
        self.limits = self.config.get('limits', {})
        self.stage_order = self.config.get('stage_order', [])
    
    def _load_config(self, config_path: str) -> dict:
        """Load circuit breaker configuration."""
        path = Path(config_path)
        if path.exists():
            with open(path) as f:
                return yaml.safe_load(f)
        # Defaults if config missing
        return {
            'limits': {
                'max_agent_invocations_per_issue': 20,
                'max_comments_per_hour': 10,
                'max_retry_attempts': 3,
                'max_issues_created_per_pr': 5,
                'max_review_cycles': 3,
            },
            'stage_order': ['triage', 'planner', 'specifier', 'simulator', 
                          'architect', 'implementer', 'tester', 'reviewer', 
                          'security', 'complete']
        }
    
    def has_marker(self, content: str, marker_type: str, **kwargs) -> bool:
        """Check if content contains a specific marker."""
        marker_template = self.MARKERS.get(marker_type, '')
        if not marker_template:
            return False
        # Replace placeholders with actual values or regex wildcards
        marker_pattern = marker_template
        for key, value in kwargs.items():
            marker_pattern = marker_pattern.replace(f'{{{key}}}', str(value))
        # Replace remaining placeholders with wildcard for checking
        marker_pattern = re.sub(r'\{[^}]+\}', r'[^>]+', marker_pattern)
        return bool(re.search(marker_pattern, content))
    
    def create_marker(self, marker_type: str, **kwargs) -> str:
        """Create a marker string with given values."""
        marker = self.MARKERS.get(marker_type, '')
        for key, value in kwargs.items():
            marker = marker.replace(f'{{{key}}}', str(value))
        return marker
    
    def count_agent_invocations(self, comments: list) -> int:
        """Count agent invocations in comment history."""
        count = 0
        for comment in comments:
            body = comment.get('body', '')
            # Count @copilot somas-* invocations (not from copilot itself)
            if '@copilot somas-' in body:
                author = comment.get('user', {}).get('login', '')
                if author not in ['copilot[bot]', 'Copilot']:
                    count += 1
        return count
    
    def count_recent_comments(self, comments: list, hours: int = 1) -> int:
        """Count comments within the last N hours."""
        from datetime import timezone
        cutoff = datetime.now(timezone.utc).replace(tzinfo=None) - timedelta(hours=hours)
        count = 0
        for comment in comments:
            created = comment.get('created_at', '')
            if created:
                try:
                    comment_time = datetime.fromisoformat(created.replace('Z', '+00:00'))
                    if comment_time.replace(tzinfo=None) > cutoff:
                        count += 1
                except ValueError:
                    pass
        return count
    
    def check_invocation_limit(self, comments: list) -> tuple[bool, str]:
        """Check if agent invocation limit reached. Returns (allowed, reason)."""
        count = self.count_agent_invocations(comments)
        limit = self.limits.get('max_agent_invocations_per_issue', 20)
        if count >= limit:
            return False, f"Max agent invocations ({limit}) reached"
        return True, ""
    
    def check_comment_rate(self, comments: list) -> tuple[bool, str]:
        """Check if comment rate limit reached. Returns (allowed, reason)."""
        count = self.count_recent_comments(comments, hours=1)
        limit = self.limits.get('max_comments_per_hour', 10)
        if count >= limit:
            return False, f"Max comments per hour ({limit}) reached"
        return True, ""
    
    def check_stage_progression(self, current_stage: str, next_stage: str) -> tuple[bool, str]:
        """Check if stage transition is valid (forward only). Returns (allowed, reason)."""
        if current_stage not in self.stage_order:
            return True, ""  # Unknown stage, allow
        if next_stage not in self.stage_order:
            return True, ""  # Unknown stage, allow
        
        current_idx = self.stage_order.index(current_stage)
        next_idx = self.stage_order.index(next_stage)
        
        if next_idx <= current_idx:
            return False, f"Backward stage transition not allowed: {current_stage} -> {next_stage}"
        return True, ""
    
    def check_all(self, comments: list, current_stage: str = None, 
                  next_stage: str = None) -> tuple[bool, str]:
        """Run all circuit breaker checks. Returns (allowed, reason)."""
        # Check invocation limit
        allowed, reason = self.check_invocation_limit(comments)
        if not allowed:
            return False, reason
        
        # Check comment rate
        allowed, reason = self.check_comment_rate(comments)
        if not allowed:
            return False, reason
        
        # Check stage progression if provided
        if current_stage and next_stage:
            allowed, reason = self.check_stage_progression(current_stage, next_stage)
            if not allowed:
                return False, reason
        
        return True, ""
    
    def get_escalation_message(self, reason: str, issue_number: int) -> str:
        """Generate escalation message when circuit breaker trips."""
        notify = self.config.get('escalation', {}).get('notify', [])
        mentions = ' '.join(f'@{user}' for user in notify)
        
        return f"""## ⚠️ Circuit Breaker Triggered

{self.create_marker('circuit_breaker', reason=reason)}

**Reason:** {reason}
**Issue:** #{issue_number}

{mentions} - Human intervention required.

The autonomous pipeline has been paused to prevent runaway automation. 
Please review the situation and manually continue if appropriate.

**To resume:** Remove the `somas:circuit-breaker` label after addressing the issue.
"""
