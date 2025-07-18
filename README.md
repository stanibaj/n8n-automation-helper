# Network Tools API

A modular FastAPI application providing network-related tools like WHOIS lookup and DNS queries.

## Features

- **WHOIS Lookup**: Get domain registration information
- **Modular Design**: Easy to add new endpoints like DNS lookup
- **Input Validation**: Validates domain format before processing
- **Error Handling**: Comprehensive error responses

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python main.py
```

The API will be available at `http://localhost:9999`

## Docker Deployment

### Prerequisites

Before running the application with Docker, you need to create the external network:

```bash
docker network create --driver bridge --subnet=192.168.18.0/24 n8n
```

### Running with Docker Compose

1. Build and run the application:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:9999`

### Running with Docker

Alternatively, you can build and run with Docker directly:

```bash
# Build the image
docker build -t n8n-automation .

# Run the container
docker run -p 9999:9999 --network n8n n8n-automation
```

### Network Management

- **List networks**: `docker network ls`
- **Inspect network**: `docker network inspect n8n`
- **Remove network**: `docker network rm n8n` (only when no containers are using it)

## API Endpoints

### GET /api/v1/whois

Perform WHOIS lookup for a domain.

**Parameters:**
- `domain` (query parameter): The domain name to lookup (e.g., example.com)

**Example:**
```bash
curl "http://localhost:9999/api/v1/whois?domain=example.com"
```

**Response:**
```json
{
  "domain": "example.com",
  "whois_data": {
    "domain_name": "EXAMPLE.COM",
    "registrar": "RESERVED-Internet Assigned Numbers Authority",
    "creation_date": "1995-08-14 04:00:00",
    "expiration_date": "2024-08-13 04:00:00",
    "name_servers": ["A.IANA-SERVERS.NET", "B.IANA-SERVERS.NET"]
  },
  "status": "success"
}
```

## Adding New Endpoints

To add a new endpoint (e.g., DNS lookup):

1. Create a new router file: `routers/dns_router.py`
2. Implement your endpoint logic
3. Add the router to `main.py`:
```python
from routers import dns_router
app.include_router(dns_router.router, prefix="/api/v1")
```

## Documentation

Once running, visit:
- API Documentation: `http://localhost:9999/docs`
- Alternative docs: `http://localhost:9999/redoc`
