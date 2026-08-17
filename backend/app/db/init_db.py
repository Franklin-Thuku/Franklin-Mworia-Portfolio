from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.project import Project
from app.core.database import Base, engine

INITIAL_PROJECTS = [
    {
        "slug": "sentinelgate",
        "serial_tag": "CASE STUDY // 01",
        "category": "SECURITY & INFRASTRUCTURE",
        "category_slug": "security backend",
        "title": "SentinelGate: Reverse Proxy & Threat Mitigator",
        "lead": "A high-throughput API gateway and defensive firewall engine designed to detect DDoS anomalies, enforce token-bucket rate limiting, and block suspicious payloads before reaching application workers.",
        "description": "SentinelGate was built to solve high-concurrency API vulnerability bottlenecks. Sitting behind TLS termination, it intercepts all incoming HTTP/gRPC streams and validates tokens with sub-millisecond memory lookups.\n\nKey Highlights:\n- Zero-allocation JSON parsing pipeline in Go reducing GC pause spikes by 84%.\n- Distributed token-bucket rate limiter backed by atomic Redis Lua scripts.\n- Cryptographic fingerprinting of malicious automated scrapers.",
        "metrics": [
            {"val": "< 3.8ms", "desc": "Median Latency Overhead"},
            {"val": "100k+ Req/s", "desc": "Simulated Load Handled"},
            {"val": "Zero-Leak", "desc": "Memory Profiling"},
            {"val": "Redis + Go", "desc": "Core Stack Engine"}
        ],
        "technologies": ["Go (Golang)", "Redis", "Docker", "Prometheus", "Linux"],
        "topology": {
            "title": "TOPOLOGY: SENTINELGATE PIPELINE",
            "version": "v2.4.1",
            "steps": [
                {"type": "node", "label": "[ CLIENT REQ ]", "sublabel": "TLS 1.3 Termination", "highlighted": False},
                {"type": "arrow", "text": "↓ inspect headers & rate-limits"},
                {"type": "node", "label": "[ SENTINEL CORE ]", "sublabel": "Go + Redis Token Bucket", "highlighted": True},
                {"type": "arrow", "text": "↓ zero-trust token validated"},
                {"type": "node", "label": "[ UPSTREAM SERVICES ]", "sublabel": "Microservices Cluster", "highlighted": False}
            ]
        },
        "github_url": "https://github.com",
        "demo_url": None,
        "is_featured": True
    },
    {
        "slug": "cortexflow",
        "serial_tag": "CASE STUDY // 02",
        "category": "APPLIED AI & DATA",
        "category_slug": "ai backend",
        "title": "CortexFlow: Vector-Augmented Knowledge Engine",
        "lead": "Enterprise-grade retrieval-augmented generation (RAG) backend that transforms complex technical documentation and codebase manuals into low-latency semantic search queries with citation validation.",
        "description": "CortexFlow prevents LLM hallucinations in mission-critical technical documentation by combining dense vector embeddings with sparse BM25 keyword matching directly inside PostgreSQL via pgvector.\n\nKey Highlights:\n- Recursive document chunker retaining hierarchical code AST context.\n- Cosine similarity clustering with automated re-ranking layer.\n- Asynchronous streaming responses via FastAPI WebSockets.",
        "metrics": [
            {"val": "94.8%", "desc": "Retrieval Precision"},
            {"val": "280ms", "desc": "End-to-End Vector Query"},
            {"val": "pgvector", "desc": "Embedding Store"},
            {"val": "Python / FastAPI", "desc": "Async REST Server"}
        ],
        "technologies": ["Python", "FastAPI", "PostgreSQL", "pgvector", "LangChain"],
        "topology": {
            "title": "TOPOLOGY: RAG VECTOR INGEST",
            "version": "v1.8.0",
            "steps": [
                {"type": "node", "label": "[ DOC INGESTION ]", "sublabel": "Markdown / PDF / Code", "highlighted": False},
                {"type": "arrow", "text": "↓ chunking & text-embedding-3"},
                {"type": "node", "label": "[ PGVECTOR STORE ]", "sublabel": "Cosine Similarity Index", "highlighted": True},
                {"type": "arrow", "text": "↓ contextual prompt synthesis"},
                {"type": "node", "label": "[ RESPONSE AGENT ]", "sublabel": "Verified Citations", "highlighted": False}
            ]
        },
        "github_url": "https://github.com",
        "demo_url": None,
        "is_featured": True
    },
    {
        "slug": "omnisync",
        "serial_tag": "CASE STUDY // 03",
        "category": "DISTRIBUTED SYSTEMS",
        "category_slug": "backend",
        "title": "OmniSync: Real-Time CRDT Collaboration Engine",
        "lead": "Conflict-free Replicated Data Type (CRDT) synchronization engine powering sub-millisecond document edits across distributed multi-tenant clients with automatic split-brain resolution.",
        "description": "OmniSync provides conflict-free distributed editing across disconnected or low-bandwidth network clients without relying on a single authoritative central lock.\n\nKey Highlights:\n- Optimized vector clocks handling out-of-order delta delivery.\n- WebSocket multiplexing with automatic exponential backoff reconnection.\n- Immutable ledger logging for full time-travel state auditability.",
        "metrics": [
            {"val": "0 Collisions", "desc": "Across 50+ Concurrent Peers"},
            {"val": "< 15ms", "desc": "WebSocket Propagation"},
            {"val": "TypeScript", "desc": "Node.js + WebSockets"},
            {"val": "PostgreSQL", "desc": "Persistent Snapshot Storage"}
        ],
        "technologies": ["TypeScript", "Node.js", "WebSockets", "PostgreSQL", "CRDT (Yjs)"],
        "topology": {
            "title": "TOPOLOGY: PEER STATE SYNC",
            "version": "v3.0.2",
            "steps": [
                {"type": "node", "label": "[ CLIENT A & B ]", "sublabel": "Local Delta Mutations", "highlighted": False},
                {"type": "arrow", "text": "↓ bidirectional WebSockets"},
                {"type": "node", "label": "[ CRDT ARBITER ]", "sublabel": "Yjs / State Vector Merge", "highlighted": True},
                {"type": "arrow", "text": "↓ debounced persistence"},
                {"type": "node", "label": "[ POSTGRES STORAGE ]", "sublabel": "Immutable Event Log", "highlighted": False}
            ]
        },
        "github_url": "https://github.com",
        "demo_url": None,
        "is_featured": True
    },
    {
        "slug": "vulcancore",
        "serial_tag": "CASE STUDY // 04",
        "category": "DEVSECOPS & CLOUD",
        "category_slug": "security backend",
        "title": "VulcanCore: Microservice Telemetry & Audit Suite",
        "lead": "Lightweight, agent-based observability sidecar collecting container metrics, distributed traces, and security event payloads with automated Slack and Webhook alerting.",
        "description": "VulcanCore is an ultra-lean systems monitor that attaches to Docker container namespaces, extracting performance metrics and audit trail logs without polluting application code.\n\nKey Highlights:\n- Tiny 2.1 MB compiled binary footprint with zero external runtime dependencies.\n- Prometheus-compatible scraping endpoints with live metric formatting.\n- Real-time rule engine alerting on anomalous permission escalations.",
        "metrics": [
            {"val": "2.1 MB", "desc": "Binary Footprint"},
            {"val": "< 0.5%", "desc": "Host CPU Utilization"},
            {"val": "Docker", "desc": "Multi-Container Deploys"},
            {"val": "Prometheus", "desc": "Metrics Formatter"}
        ],
        "technologies": ["Docker", "Prometheus", "Python", "Linux", "CI/CD"],
        "topology": {
            "title": "TOPOLOGY: SIDECAR TELEMETRY",
            "version": "v1.2.4",
            "steps": [
                {"type": "node", "label": "[ APP CONTAINER ]", "sublabel": "stdout / stderr / sockets", "highlighted": False},
                {"type": "arrow", "text": "↓ zero-overhead unix domain pipe"},
                {"type": "node", "label": "[ VULCAN AGENT ]", "sublabel": "Log Parsing & Anomaly Rule", "highlighted": True},
                {"type": "arrow", "text": "↓ cryptographically signed ingest"},
                {"type": "node", "label": "[ AUDIT DASHBOARD ]", "sublabel": "Secure Telemetry Store", "highlighted": False}
            ]
        },
        "github_url": "https://github.com",
        "demo_url": None,
        "is_featured": True
    }
]


async def init_db(session: AsyncSession) -> None:
    # Check if projects exist
    result = await session.execute(select(Project))
    existing = result.scalars().all()
    if not existing:
        for p_data in INITIAL_PROJECTS:
            project = Project(**p_data)
            session.add(project)
        await session.commit()
        print("[DB INIT] Seeded initial portfolio projects successfully.")
