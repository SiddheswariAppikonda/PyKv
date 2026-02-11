from collections import OrderedDict

# Global counters for stats
cache_hits = 0
cache_misses = 0

class LRUCache:
    def __init__(self, capacity: int = 5):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key):
        global cache_hits, cache_misses
        if key not in self.cache:
            cache_misses += 1
            return None

        # Mark as recently used
        self.cache.move_to_end(key)
        cache_hits += 1
        return self.cache[key]

    def put(self, key, value):
        evicted_key = None

        # Update existing key
        if key in self.cache:
            self.cache.move_to_end(key)

        # Insert / update
        self.cache[key] = value

        # Evict LRU if capacity exceeded
        if len(self.cache) > self.capacity:
            evicted_key, _ = self.cache.popitem(last=False)

        return evicted_key

    def delete(self, key):
        if key in self.cache:
            del self.cache[key]

    def keys(self):
        """Return cache keys in LRU order (for debugging/UI)"""
        return list(self.cache.keys())

    def get_all(self):
        """Return full cache contents"""
        return dict(self.cache)


# Helper function to get stats for frontend
def get_cache_stats(lru_cache_instance: LRUCache):
    total_keys = len(lru_cache_instance.cache)
    hits = cache_hits
    misses = cache_misses
    performanceRate = round((hits / (hits + misses) * 100) if (hits + misses) > 0 else 0, 2)

    return {
        "totalKeys": total_keys,
        "hits": hits,
        "misses": misses,
        "performanceRate": performanceRate
    }
