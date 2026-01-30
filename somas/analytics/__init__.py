"""
SOMAS Analytics Module.

This module provides metrics tracking, analysis, and reporting for the SOMAS
autonomous pipeline. It captures data to demonstrate value, optimize performance,
and enable continuous learning.

Components:
    poc_metrics: Proof-of-concept metrics tracking
        - Time savings calculation
        - Autonomy percentage measurement
        - ROI analysis
        - Quality improvements tracking

    cost_tracker: Model usage and effectiveness tracking
        - Token usage monitoring
        - Success rate tracking
        - Usage pattern analysis

Key Metrics:
    Time Savings:
        - Total duration vs manual estimate
        - Time saved percentage
        - Stage-by-stage breakdown

    Quality Improvements:
        - Test coverage percentage
        - First-shot success rate
        - Code review scores

    Human Effort Reduction:
        - Human intervention count
        - Autonomous execution percentage
        - Escalation frequency

    ROI Analysis:
        - Value of time saved
        - Subscription cost
        - Return on investment percentage

Storage:
    Analytics data is stored in ``.somas/analytics/``:

    - ``runs/``: Individual pipeline run data
    - ``poc/``: Proof-of-concept reports
    - ``usage/``: Model usage logs
    - ``apo/``: APO performance metrics

Example:
    Using the POC metrics tracker::

        from somas.analytics.poc_metrics import ProofOfConceptMetrics

        tracker = ProofOfConceptMetrics()
        tracker.track_project_completion({
            'id': 'project-123',
            'duration_mins': 60,
            'test_coverage': 85.0,
            'human_interventions': 1
        })
        report = tracker.generate_poc_report()

Configuration:
    Analytics settings in ``.somas/config.yml``::

        analytics:
          enabled: true
          storage: ".somas/analytics/runs/"
          retention_days: 90
          track:
            - "task_duration_vs_estimate"
            - "parallel_efficiency"

See Also:
    - docs/somas/optimization-guide.md for optimization techniques
    - .somas/analytics/schema.yml for metrics schema
"""

__all__ = []
