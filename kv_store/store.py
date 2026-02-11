# core/store.py
import asyncio
import requests
from kv_store.lru_cache import LRUCache, get_cache_stats
from kv_store.persistence import Persistence

REPLICA_URL = "http://127.0.0.1:8001"


class PyKVStore:
    def __init__(self, is_primary=True, enable_persistence=True, log_file="data.log"):
        self.is_primary = is_primary
        self.cache = LRUCache(capacity=5)
        self.store = {}

        self.enable_persistence = enable_persistence
        self.persistence = Persistence(log_file) if enable_persistence else None

        # Recover data from disk (only if persistence enabled)
        if self.persistence:
            recovered_data = self.persistence.load()
            self.store.update(recovered_data)

    # ========================
    # CRUD METHODS
    # ========================

    async def get(self, key: str):
        await asyncio.sleep(0)

        value = self.cache.get(key)
        if value is not None:
            return value

        value = self.store.get(key)
        if value is not None:
            self.cache.put(key, value)

        return value

    async def set(self, key: str, value: str):
        await asyncio.sleep(0)

        self.store[key] = value
        evicted_key = self.cache.put(key, value)

        # Persist only if enabled
        if self.persistence:
            self.persistence.write(key, value)

        # Replicate only if primary
        if self.is_primary:
            await self._replicate("set", key, value)

        return evicted_key

    async def delete(self, key: str):
        await asyncio.sleep(0)

        self.cache.delete(key)

        if key in self.store:
            del self.store[key]

            if self.persistence:
                self.persistence.write_delete(key)

            if self.is_primary:
                await self._replicate("delete", key)

            return True

        return False

    async def get_all(self):
        await asyncio.sleep(0)
        return self.store

    # ========================
    # CACHE STATS
    # ========================

    def get_cache_stats(self):
        """
        Return cache statistics for the frontend.
        totalKeys, hits, misses, performanceRate
        """
        return get_cache_stats(self.cache)

    # ========================
    # REPLICATION
    # ========================

    async def _replicate(self, action, key, value=None):
        if not await self._is_replica_alive():
            print("[Replication] Replica down. Will retry...")
            await self._retry_replication(action, key, value)
            return

        payload = {"action": action, "key": key}
        if value is not None:
            payload["value"] = value

        try:
            requests.post(f"{REPLICA_URL}/replicate", json=payload, timeout=2)
        except Exception as e:
            print("[Replication] Failed:", e)
            await self._retry_replication(action, key, value)

    async def _is_replica_alive(self):
        try:
            res = requests.get(f"{REPLICA_URL}/health", timeout=1)
            return res.status_code == 200
        except:
            return False

    async def _retry_replication(self, action, key, value):
        for i in range(3):
            await asyncio.sleep(2)
            if await self._is_replica_alive():
                payload = {"action": action, "key": key}
                if value is not None:
                    payload["value"] = value
                try:
                    requests.post(f"{REPLICA_URL}/replicate", json=payload, timeout=2)
                    print("[Replication] Success on retry", i + 1)
                    return
                except:
                    pass
        print("[Replication] Replica unreachable after retries.")
