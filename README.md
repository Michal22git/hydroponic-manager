# Hydroponic System Management API 🌱

## Table of Contents

1. [Introduction](#introduction)
2. [Key Features](#key-features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [API Documentation](#api-documentation)

## Introduction

This repository contains a recruitment task implementation - a REST API for managing hydroponic cultivation systems. The main goal is to demonstrate CRUD operations implementation using Django REST Framework.

## Key Features

### Authentication & Authorization
- JWT token authentication
- User registration with password validation
- Token refresh mechanism

### Hydroponic System Management
- CRUD operations for hydroponic systems
- Advanced filtering options
- Pagination with customizable page sizes

### Measurement Management
- Sensor data storage: pH, TDS, water temperature
- Advanced filtering
- Multi-field sorting capabilities
- Automatic timestamping for measurements

## Tech Stack

**Core Components:**
- Python 3.11
- Django 5.1
- Django REST Framework
- PostgreSQL 15
- Docker
- DRF Simple JWT
- DRF Yasg


## Installation

### Prerequisites
- Docker & Docker Compose
- Python 3.11+
- PostgreSQL client

### Setup Steps

1. **Clone repository:**
   ```bash
   git clone https://github.com/Michal22git/hydroponic-manager
   cd hydroponic-manager
   ```

2. **Environment configuration:**
   ```bash
   echo "POSTGRES_DB=hydroponic
   POSTGRES_USER=admin
   POSTGRES_PASSWORD=secret
   POSTGRES_PORT=5432
   POSTGRES_HOST=db" > .env
   ```

3. **Start services:**
   ```bash
   docker-compose up --build
   ```

## API Documentation

Interactive API documentation available at `/swagger/` and `/redoc/` endpoints. Includes:
- Complete list of endpoints
- Request/response schemas
- Authentication requirements
- Direct testing interface

### Core Endpoints

**Authentication:**
```http
POST /api/user/register/ - User registration
POST /api/user/login/ - Obtain JWT tokens
POST /api/user/refresh/ - Refresh access token
```

**Systems:**
```http
GET    /api/systems/ - List all systems
POST   /api/systems/ - Create new system
GET    /api/systems/{id}/ - Get system details
PUT    /api/systems/{id}/ - Update system
DELETE /api/systems/{id}/ - Delete system
```

**Measurements:**
```http
GET    /api/measurements/ - List all measurements
POST   /api/measurements/ - Create new measurement
GET    /api/measurements/{id}/ - Get measurement details
```

### Advanced Filtering

**Systems Endpoint:**
```http
GET /api/systems/?search=greenhouse&created_at__gte=2025-01-01&ordering=-created_at
```

| Parameter             | Type    | Description                          |
|-----------------------|---------|--------------------------------------|
| `search`              | string  | Search in name/description (partial) |
| `created_at__[gte/lte]` | date   | Date range filtering (ISO format)   |
| `ordering`            | string  | Sort fields (-field for descending) |

**Measurements Endpoint:**
```http
GET /api/measurements/?ph_min=6.5&ph_max=7.5&tds_min=500&temperature_max=30&created_at_after=2025-01-01&ordering=-created_at,ph
```

| Parameter                   | Type     | Description                          |
|-----------------------------|----------|--------------------------------------|
| `ph_min`/`ph_max`           | float    | pH range (0.0-14.0)                 |
| `tds_min`/`tds_max`         | integer  | TDS value range                     |
| `temperature_min`/`temperature_max` | float | Water temperature range          |
| `created_at_after`          | datetime | Measurements after timestamp        |
| `created_at_before`         | datetime | Measurements before timestamp       |
| `ordering`                  | string   | Sort fields (-field for descending) |

### Example Requests

**Create System:**
```bash
curl -X POST "http://localhost:8000/api/systems/" \
  -H "Authorization: Bearer your_jwt_token" \
  -H "Content-Type: application/json" \
  -d '{"name": "Main Greenhouse", "description": "Primary cultivation system"}'
```

**Get Filtered Measurements:**
```bash
curl -X GET "http://localhost:8000/api/measurements/?ph_min=6.0&ph_max=7.0&ordering=-created_at" \
  -H "Authorization: Bearer your_jwt_token"
```

    
