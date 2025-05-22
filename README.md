# Loan Application Processing

## Prerequisites

Before running the project, make sure you have the following installed:

### 1. **Docker**
Ensure that you have **Docker** and **Docker Compose** installed to easily run the project in a containerized environment.

- **[Docker installation](https://docs.docker.com/get-docker/)**
- **[Docker Compose installation](https://docs.docker.com/compose/install/)**

### 2. **Python 3.11+**
Ensure that you have **Python 3.11+** installed for running the project locally.

- **[Python installation](https://www.python.org/downloads/)**

### 3. **Kafka & Redis (For Local Development)**
This project uses **Kafka** and **Redis** for messaging and caching. These services are handled via Docker Compose, so you don’t need to install them locally.

- **Kafka**: Message broker for handling loan applications.
- **Redis**: In-memory caching for loan application status.

### 4. **.env File**
The project requires environment variables for various configurations, including the database, Kafka, and Redis URLs. You can find a sample **`.env`** file in the repository, or you can create one with the following variables:

```env
DATABASE_URL=postgresql://user:password@postgres:5432/loan_db
TEST_DATABASE_URL=postgresql://user:password@postgres:5432/test_loan_db
KAFKA_URL=kafka:9092
REDIS_URL=redis://redis:6379



# Installation Guide

## 1. Clone the Repository
Clone the project repository to your local machine:

```bash
git clone <repository_url>
cd <project_directory>
```

## Installation Guide

### 2. Build and Start the Docker Containers
Use Docker Compose to build and run the application with all necessary services (FastAPI, PostgreSQL, Kafka, Redis):

```bash
docker-compose up --build
```

This command will:

- Build the Docker images for the project.
- Start the FastAPI server, PostgreSQL, Kafka, and Redis containers.

The server will be running on `http://localhost:8000`.

## 3. Install Python Dependencies Locally (Optional)
If you need to run the project without Docker or want to run tests locally, you can install the required Python dependencies:

```bash
pip install -r requirements.txt
```

# Starting the Server

After running `docker-compose up --build`, the FastAPI server will be accessible at:

```bash
http://localhost:8000
```

You can start the server manually if needed (for non-Docker setup):

```bash
uvicorn app.main:app --reload
```

# Accessing the Swagger Docs

FastAPI provides interactive API documentation through Swagger. Once the server is running, you can access it at:

```bash
http://localhost:8000/docs
```

Here you will find:

- API endpoints for applying for loans, getting loan statuses, etc.
- The ability to test endpoints directly from the browser.

# Running the Tests

The project uses `pytest` to run the tests.

## 1. Run Tests Inside Docker Container

To run the tests inside the Docker container, execute the following command:

```bash
docker-compose exec it <container_id> pytest . 
```

This will:

- Run the tests inside the container.
- Show you the output of the tests in your terminal.
