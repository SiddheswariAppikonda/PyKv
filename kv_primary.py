from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kv_store.store import PyKVStore
from models.request_models import SetRequest
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ========================
# STORES
# ========================

# REAL USER STORE (persistent + replicated)
db = PyKVStore(
    is_primary=True,
    enable_persistence=True,
    log_file="data.log"
)

# BENCHMARK STORE (NO persistence, NO replication)
bench_db = PyKVStore(
    is_primary=False,
    enable_persistence=False
)

# ========================
# USER APIs
# ========================

@app.get("/get/{key}")
async def get_value(key: str):
    value = await db.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"key": key, "value": value}

@app.post("/set")
async def set_value(req: SetRequest):
    cache_before = list(db.cache.cache.keys())
    evicted_key = await db.set(req.key, req.value)
    cache_after = list(db.cache.cache.keys())

    return {
        "message": f"Key '{req.key}' set successfully",
        "cache_before_set": cache_before,
        "cache_after_set": cache_after,
        "evicted_key": evicted_key
    }

@app.delete("/delete/{key}")
async def delete_value(key: str):
    success = await db.delete(key)
    if not success:
        raise HTTPException(status_code=404, detail="Key not found")
    return {"message": f"Key '{key}' deleted successfully"}

@app.get("/all")
async def get_all_values():
    return {
        "full_store": db.store,
        "current_cache": list(db.cache.cache.keys())
    }

# ========================
# BENCHMARK API
# ========================

@app.post("/benchmark/run")
async def run_benchmark(ops: int = 1000):
    bench_db.store.clear()
    bench_db.cache.cache.clear()

    start = time.time()

    for i in range(ops):
        await bench_db.set(f"bench_{i}", f"value_{i}")

    end = time.time()

    return {
        "operations": ops,
        "time_seconds": round(end - start, 3),
        "ops_per_second": round(ops / (end - start), 2),
        "latency_ms_per_op": round(((end - start) / ops) * 1000, 4)
    }

# ========================
# HEALTH
# ========================

@app.get("/health")
def health():
    return {"status": "ok", "role": "primary"}


# ========================
# CACHE STATS
# ========================

@app.get("/cache-stats")
def cache_stats():
    # Use the method we added in PyKVStore
    return db.get_cache_stats()
