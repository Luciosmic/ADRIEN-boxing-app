from .metrics_collector import MetricsCollector

class EventStoreMetrics:
    """
    Specific metrics for the EventStore as requested.
    """
    def __init__(self, collector: MetricsCollector):
        self._collector = collector

    def record_append(self, count: int = 1):
        self._collector.increment("event_store.events_appended", count)

    def record_read(self, count: int = 1):
        self._collector.increment("event_store.streams_read", count)
