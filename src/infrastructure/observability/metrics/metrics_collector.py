from typing import Dict

class MetricsCollector:
    """
    Simple metrics collector facade.
    Can be swapped for Prometheus/StatsD later.
    """
    def __init__(self):
        self._counters: Dict[str, int] = {}

    def increment(self, metric: str, value: int = 1):
        if metric not in self._counters:
            self._counters[metric] = 0
        self._counters[metric] += value

    def get_metric(self, metric: str) -> int:
        return self._counters.get(metric, 0)
