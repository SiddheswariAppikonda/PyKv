from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from kv_store.store import PyKVStore
from models.replica_request_models import ReplicateRequest

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Replica store (YES persistence, NO replication)
replica_db = PyKVStore(
    is_primary=False,
    enable_persistence=True,
    log_file="replica.log"
)

# -------------------------
# Recovery on Startup
# -------------------------
@app.on_event("startup")
async def load_replica_data():
    recovered_data = replica_db.persistence.load()
    replica_db.store.update(recovered_data)
    for k, v in recovered_data.items():
        replica_db.cache.put(k, v)


@app.post("/replicate")
async def replicate_operation(req: ReplicateRequest):
    if req.action == "set":
        await replica_db.set(req.key, req.value)
    elif req.action == "delete":
        await replica_db.delete(req.key)

    return {"status": "replicated"}


@app.get("/get/{key}")
async def get_from_replica(key: str):
    value = await replica_db.get(key)
    if value is None:
        raise HTTPException(status_code=404, detail="Key not found in replica")
    return {"key": key, "value": value}


@app.get("/health")
def health():
    return {"status": "ok", "role": "replica"}
