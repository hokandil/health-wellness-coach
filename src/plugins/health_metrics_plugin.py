"""
Health Metrics Plugin for ADK

Custom plugin to track health-specific metrics including:
- Query counts per domain (nutrition, fitness, sleep, wellness)
- Tool usage statistics
- Response times
- Agent routing patterns
"""

import time
import logging
from typing import Dict, Any, Optional
from collections import defaultdict, Counter

from google.adk.plugins import Plugin

logger = logging.getLogger(__name__)


class HealthMetricsPlugin(Plugin):
    """
    Custom ADK plugin for tracking health-specific metrics.
    
    This plugin monitors:
    - Domain-specific query counts
    - Tool invocation frequency
    - Agent routing decisions
    - Response time statistics
    """
    
    def __init__(self):
        """Initialize the Health Metrics Plugin."""
        super().__init__()
        
        # Metrics storage
        self.domain_queries = Counter()  # nutrition, fitness, sleep, wellness
        self.tool_usage = Counter()  # tool function names
        self.agent_routing = Counter()  # which agents were invoked
        self.response_times = []  # list of response times in seconds
        self.total_queries = 0
        self.error_count = 0
        
        # Timing
        self._query_start_time: Optional[float] = None
        
        logger.info("HealthMetricsPlugin initialized")
    
    def on_run_start(self, context: Dict[str, Any]):
        """Called when a query execution starts."""
        self._query_start_time = time.time()
        self.total_queries += 1
        logger.debug(f"Query started: {context.get('user_message', '')[:50]}...")
    
    def on_run_end(self, context: Dict[str, Any]):
        """Called when a query execution completes."""
        if self._query_start_time:
            elapsed = time.time() - self._query_start_time
            self.response_times.append(elapsed)
            logger.debug(f"Query completed in {elapsed:.2f}s")
            self._query_start_time = None
    
    def on_tool_call(self, context: Dict[str, Any]):
        """Called when a tool is invoked."""
        tool_name = context.get('tool_name', 'unknown')
        self.tool_usage[tool_name] += 1
        
        # Track domain based on tool name
        if 'nutrition' in tool_name.lower():
            self.domain_queries['nutrition'] += 1
        elif 'fitness' in tool_name.lower() or 'workout' in tool_name.lower():
            self.domain_queries['fitness'] += 1
        elif 'sleep' in tool_name.lower():
            self.domain_queries['sleep'] += 1
        elif 'wellness' in tool_name.lower() or 'stress' in tool_name.lower():
            self.domain_queries['mental_wellness'] += 1
        
        logger.debug(f"Tool called: {tool_name}")
    
    def on_agent_call(self, context: Dict[str, Any]):
        """Called when a sub-agent is invoked."""
        agent_name = context.get('agent_name', 'unknown')
        self.agent_routing[agent_name] += 1
        
        # Track domain based on agent name
        if 'nutrition' in agent_name.lower():
            self.domain_queries['nutrition'] += 1
        elif 'fitness' in agent_name.lower():
            self.domain_queries['fitness'] += 1
        elif 'sleep' in agent_name.lower():
            self.domain_queries['sleep'] += 1
        elif 'wellness' in agent_name.lower():
            self.domain_queries['mental_wellness'] += 1
        
        logger.debug(f"Agent invoked: {agent_name}")
    
    def on_error(self, context: Dict[str, Any]):
        """Called when an error occurs."""
        self.error_count += 1
        error = context.get('error', 'Unknown error')
        logger.warning(f"Error occurred: {error}")
    
    def get_metrics(self) -> Dict[str, Any]:
        """
        Get all collected metrics.
        
        Returns:
            Dictionary containing all health metrics
        """
        avg_response_time = (
            sum(self.response_times) / len(self.response_times)
            if self.response_times else 0
        )
        
        return {
            'total_queries': self.total_queries,
            'error_count': self.error_count,
            'error_rate': self.error_count / max(self.total_queries, 1),
            'domain_queries': dict(self.domain_queries),
            'tool_usage': dict(self.tool_usage),
            'agent_routing': dict(self.agent_routing),
            'avg_response_time_seconds': round(avg_response_time, 2),
            'min_response_time_seconds': round(min(self.response_times), 2) if self.response_times else 0,
            'max_response_time_seconds': round(max(self.response_times), 2) if self.response_times else 0,
            'total_response_count': len(self.response_times)
        }
    
    def reset_metrics(self):
        """Reset all metrics to initial state."""
        self.domain_queries.clear()
        self.tool_usage.clear()
        self.agent_routing.clear()
        self.response_times.clear()
        self.total_queries = 0
        self.error_count = 0
        logger.info("Health metrics reset")
    
    def export_metrics(self, filepath: str):
        """
        Export metrics to a JSON file.
        
        Args:
            filepath: Path to export metrics to
        """
        import json
        from pathlib import Path
        
        metrics = self.get_metrics()
        
        Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Metrics exported to {filepath}")
