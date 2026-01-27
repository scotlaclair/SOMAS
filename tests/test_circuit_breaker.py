"""Tests for circuit breaker infrastructure."""

import pytest
from datetime import datetime, timedelta
from somas.core.circuit_breaker import CircuitBreaker


class TestCircuitBreaker:
    
    def test_marker_creation(self):
        cb = CircuitBreaker()
        marker = cb.create_marker('pr_continue', pr_number=26)
        assert marker == '<!-- SOMAS_PR_CONTINUE:PR-26 -->'
    
    def test_marker_detection(self):
        cb = CircuitBreaker()
        content = "Some text <!-- SOMAS_PR_CONTINUE:PR-26 --> more text"
        assert cb.has_marker(content, 'pr_continue', pr_number=26)
        assert not cb.has_marker(content, 'pr_continue', pr_number=27)
    
    def test_marker_detection_wildcard(self):
        cb = CircuitBreaker()
        content = "<!-- SOMAS_RECOMMENDATIONS_CAPTURED:5 -->"
        assert cb.has_marker(content, 'recommendations_captured')
    
    def test_count_agent_invocations(self):
        cb = CircuitBreaker()
        comments = [
            {'body': '@copilot somas-architect please review', 'user': {'login': 'scotlaclair'}},
            {'body': 'Here is my review...', 'user': {'login': 'copilot[bot]'}},
            {'body': '@copilot somas-tester please test', 'user': {'login': 'github-actions[bot]'}},
        ]
        # Should count 2 (not the copilot response)
        assert cb.count_agent_invocations(comments) == 2
    
    def test_invocation_limit_not_reached(self):
        cb = CircuitBreaker()
        comments = [{'body': '@copilot somas-test', 'user': {'login': 'user'}}] * 5
        allowed, reason = cb.check_invocation_limit(comments)
        assert allowed
        assert reason == ""
    
    def test_invocation_limit_reached(self):
        cb = CircuitBreaker()
        comments = [{'body': '@copilot somas-test', 'user': {'login': 'user'}}] * 25
        allowed, reason = cb.check_invocation_limit(comments)
        assert not allowed
        assert "Max agent invocations" in reason
    
    def test_stage_progression_forward(self):
        cb = CircuitBreaker()
        allowed, reason = cb.check_stage_progression('architect', 'tester')
        assert allowed
    
    def test_stage_progression_backward_blocked(self):
        cb = CircuitBreaker()
        allowed, reason = cb.check_stage_progression('tester', 'architect')
        assert not allowed
        assert "Backward stage transition" in reason
    
    def test_stage_progression_same_blocked(self):
        cb = CircuitBreaker()
        allowed, reason = cb.check_stage_progression('tester', 'tester')
        assert not allowed
    
    def test_comment_rate_limit(self):
        cb = CircuitBreaker()
        now = datetime.utcnow()
        comments = [
            {'body': 'test', 'created_at': (now - timedelta(minutes=i)).isoformat() + 'Z'}
            for i in range(15)
        ]
        allowed, reason = cb.check_comment_rate(comments)
        assert not allowed
        assert "Max comments per hour" in reason
