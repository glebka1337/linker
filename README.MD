# Linker API

Linker is a high-performance, asynchronous REST API designed for intelligent note management. It implements a distributed architecture to handle semantic search via vector embeddings, asynchronous background processing, and secure multi-tenant data storage.

The system is built using Python 3.12 and follows strict Clean Architecture principles to ensure scalability, maintainability, and testability.

## System Architecture

The project adopts a Modular Monolith architecture with distinct entry points for the API and background workers, sharing a common domain kernel.

### Core Components

1. **API Gateway (FastAPI):** Handles HTTP requests, authentication, and request validation. It delegates logic to the Service Layer and Repositories.
2. **Asynchronous Workers:**
* **Linker Worker:** Manages logical connections between entities.
* **Vectorizer Worker:** Consumes messages from RabbitMQ to generate vector embeddings for note content.


3. **ML Microservice:** A dedicated, containerized service running PyTorch and Sentence Transformers. It exposes an internal HTTP endpoint for generating embeddings, isolating heavy ML dependencies from the main application core.
4. **Message Broker (RabbitMQ):** Decouples the API from resource-intensive vectorization tasks.
5. **Data Storage:**
* **MongoDB:** Primary document store for user profiles and notes. Data access is abstracted via the Repository Pattern using Beanie ODM.
* **Qdrant:** Vector database used for storing high-dimensional embeddings and performing semantic similarity searches.



## Technology Stack

* **Language:** Python 3.12
* **Web Framework:** FastAPI
* **Database:** MongoDB (Motor/Beanie)
* **Vector Database:** Qdrant
* **Message Broker:** RabbitMQ (aio-pika)
* **Machine Learning:** PyTorch, Sentence Transformers
* **Authentication:** JWT (Access/Refresh Token Rotation), Bcrypt
* **Containerization:** Docker, Docker Compose
* **Dependency Management:** Poetry

## Features

* **Clean Architecture:** Strict separation of concerns (Entities, Use Cases, Interface Adapters).
* **Secure Authentication:** Implementation of JWT standards with short-lived access tokens and secure refresh token rotation. Password hashing via Bcrypt.
* **Multi-tenancy:** All data access is strictly scoped to the authenticated user's UUID.
* **Asynchronous Processing:** Non-blocking API operations where heavy tasks (vectorization) are offloaded to background queues.
* **Semantic Search:** Capability to query notes based on meaning rather than exact keyword matches.
* **Production-Ready Docker Setup:** Optimized multi-stage builds using `python-slim` images, reducing image size and build time.

## Installation and Deployment

The project is designed to be run in a containerized environment.

### Prerequisites

* Docker Engine
* Docker Compose

### Configuration

Create a `.env` file in the root directory. The application requires the following environment variables:

```ini
# Database Configuration
DB_USER=root
DB_PASSWORD=example
DB_NAME=linker_db
DB_HOST=mongo_db

# Security
SECRET_KEY=your_secure_random_string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# RabbitMQ Configuration
RABBITMQ_DEFAULT_USER=guest
RABBITMQ_DEFAULT_PASS=guest
RABBITMQ_HOST=rabbit_queue

# Vector Database
QDRANT_HOST=qdrant_db
QDRANT_PORT=6333

# ML Service Configuration
ML_SERVICE_URL=http://ml_service:8000
ML_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

```

### Building and Running

To start the entire system, including databases and workers, use Docker Compose:

```bash
# Build and start services in detached mode
docker compose up -d --build

```

This command will:

1. Initialize the MongoDB and Qdrant containers.
2. Start the RabbitMQ message broker.
3. Build the lightweight API/Worker image.
4. Build the heavy ML Service image (downloading necessary models).
5. Start the API, Workers, and ML Service.

### Development Mode

For local development with hot-reloading, ensure `docker-compose.override.yml` is present (mapping local source volumes) and run:

```bash
docker-compose up

```

## API Documentation

Once the services are running, the OpenAPI (Swagger) documentation is available at:

```
http://localhost:8000/docs

```

### Key Endpoints

* **Auth:**
* `POST /auth/register`: Create a new user account.
* `POST /auth/login`: Authenticate and receive Access/Refresh tokens.
* `POST /auth/refresh`: Rotate refresh tokens to obtain a new session.


* **Notes:**
* `POST /notes/`: Create a note (triggers async vectorization).
* `GET /notes/{uuid}`: Retrieve a specific note.
* `PATCH /notes/{uuid}`: Update note content.
* `DELETE /notes/{uuid}`: Remove a note.



## Testing

The repository includes a comprehensive integration smoke test script that verifies the entire pipeline (Auth -> DB -> API).

To run the test against a running Docker instance:

```bash
# Ensure jq is installed for JSON parsing
chmod +x test/smoke_test.sh
./test/smoke_test.sh

```

This script will dynamically generate a user, perform authentication flow, manipulate data, and assert the correct HTTP status codes.

## Project Structure

```text
.
├── src
│   ├── core            # Domain Entities and Config
│   ├── db              # Database connection logic
│   ├── di              # Dependency Injection containers
│   ├── interfaces      # Protocols and Abstract Base Classes
│   ├── models          # Database Documents (Beanie/ODM)
│   ├── repos           # Data Access Layer implementation
│   ├── routers         # HTTP Controllers
│   ├── schemas         # Pydantic DTOs
│   ├── services        # Domain Services (Auth, Vectorizer)
│   ├── usecases        # Application Business Logic
│   ├── utils           # Shared utilities
│   └── workers         # Background task consumers
├── ml_api_service      # Isolated ML Microservice
├── tests               # Integration tests
├── Dockerfile          # Main application build
├── Dockerfile.ml       # ML service build
└── docker-compose.yml  # Orchestration

```