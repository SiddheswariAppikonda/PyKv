# PyKv - A Distributed Persistent Key-Value Store

PyKv is a lightweight Python-based key-value store that combines **caching for performance**, **persistence for durability**, and **replication for high availability**.  
The system follows a **Primary–Replica architecture** to ensure fault tolerance and efficient data management.

## Features
- Key-value data storage
- Fast caching mechanism
- Persistent storage using log files
- Primary–Replica replication
- Failover handling when the primary server goes down
- Web-based dashboard for monitoring operations

## Project Structure
```
PyKv/
│
├── auth_service/        # Authentication logic
├── frontend/            # Web interface
├── kv_store/            # Key-value storage logic
├── models/              # Data models
├── output_screenshots/  # Project screenshots
│
├── client.py
├── kv_primary.py
├── kv_replica.py
├── start_servers.bat
└── README.md
```

## Screenshots
Project screenshots are available in the `output_screenshots` folder.

## How to Run

1. Clone the repository
2. Start the primary server

```
python kv_primary.py
```

3. Start the replica server

```
python kv_replica.py
```