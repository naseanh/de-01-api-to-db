# Architecture

## Overview

This project implements a simple, end-to-end ETL (Extract → Transform → Load) pipeline that ingests weather data from an external API and stores it in a PostgreSQL database.

The system is designed to demonstrate:

- Data ingestion from an external service
- Data transformation and normalization
- Persistent storage in a relational database
- Query-based data retrieval

## System Context

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Open-Meteo API]:::api -->|HTTP JSON| B[pipeline.py]:::app
    B ==>|INSERT via psycopg2| C[(PostgreSQL)]:::db

    D[DataGrip]:::tool -.->|Query| C
    C -->|Response| D

    classDef api fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff
    classDef tool fill:#aaaaaa,color:#000

    linkStyle 0 stroke:#1f77b4,stroke-width:2px
    linkStyle 1 stroke:#2ca02c,stroke-width:3px
    linkStyle 2 stroke:#999999,stroke-dasharray: 5 5
    linkStyle 3 stroke:#555555,stroke-width:2px
```

## Description

- **Open-Meteo API**: External data source providing weather data
- **pipeline.py**: Core application responsible for ETL logic
- **PostgreSQL**: Persistent storage layer
- **DataGrip**: Tool used for querying and validating stored data

## ETL Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[Extract]:::step --> B[Transform]:::step
    B --> C[Load]:::step
    C --> D[(weather_observations table)]:::db

    classDef step fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#888888,stroke-width:1.5px
    linkStyle 1 stroke:#888888,stroke-width:1.5px
    linkStyle 2 stroke:#2ca02c,stroke-width:3px
```

## ETL Flow Description

1. Extract
    - Sends HTTP request to Open-Meteo API
    - Retrieves JSON payload
2. Transform
    - Extracts relevant fields
    - Converts units:
      - Celsius → Fahrenheit
      - km/h → mph
    - Normalizes data structure
3. Load
    - Inserts record into PostgreSQL
    - Uses ON CONFLICT to prevent duplicates

## Execution Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[run_pipeline]:::app --> B[extract]:::app
    B --> C[transform]:::app
    C --> D[load]:::app
    D --> E[(PostgreSQL)]:::db

    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#888888
    linkStyle 1 stroke:#888888
    linkStyle 2 stroke:#888888
    linkStyle 3 stroke:#2ca02c,stroke-width:3px
```

## Execution Flow Description

- `run_pipeline()` orchestrates execution
- Each function represents a distinct pipeline stage
- Data flows sequentially through the system

## Data Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart LR
    A[Raw API JSON]:::api --> B[Parsed Data]:::app
    B:::app --> C[Transformed Record]:::app
    C --> D[(PostgreSQL Row)]:::db

    classDef api fill:#1f77b4,color:#fff
    classDef app fill:#ff7f0e,color:#000
    classDef db fill:#2ca02c,color:#fff

    linkStyle 0 stroke:#1f77b4
    linkStyle 1 stroke:#ff7f0e
    linkStyle 2 stroke:#2ca02c,stroke-width:2px
```

## Data Flow Description

- Raw API response is parsed into Python structures
- Data is transformed into a normalized record
- Record is inserted into the database

## Configuration Flow

```mermaid
%%{init: {'theme': 'base'}}%%
flowchart TD
    A[.env file] --> B[load_dotenv]
    B --> C[os.getenv]
    C --> D[DB_CONFIG / API_PARAMS]
    D --> E[pipeline.py execution]

    classDef config fill:#aaaaaa,color:#000
    classDef app fill:#ff7f0e,color:#000

    class A,B,C,D config
    class E app

    linkStyle 0 stroke:#bbbbbb,stroke-width:1.5px
    linkStyle 1 stroke:#bbbbbb,stroke-width:1.5px
    linkStyle 2 stroke:#bbbbbb,stroke-width:1.5px
    linkStyle 3 stroke:#bbbbbb,stroke-width:1.5px
```

## Configuration Flow Description

- Environment variables define runtime configuration
- Supports default + override pattern:
  - DEFAULT_* → fallback
  - WEATHER_* → runtime override

## Key Design Decisions

1. Environment-Based Configuration
    - Avoids hardcoding values
    - Enables flexible deployment
2. Idempotent Data Loading
    - UNIQUE (location, observed_at)
    - ON CONFLICT DO NOTHING
    - Prevents duplicate records
3. Separation of Concerns
    - Extract, Transform, Load are independent functions
    - Improves readability and maintainability
4. Context Managers for DB Access
    - Uses `with psycopg3.connect()` and `with conn.cursor()`
    - Ensures automatic cleanup of connections and cursors
    - Prevents resource leaks and connection exhaustion

## Limitations (Phase 1)

- Single location ingestion
- No retry logic for API failures
- No scheduling or automation
- No structured logging
- No connection pooling

## Future Enhancements (Phase 2+)

- Multi-location ingestion
- Scheduled pipeline execution (cron / scheduler)
- Retry and backoff for API calls
- Structured logging (JSON logs)
- Modular architecture (api, db, config layers)
- API layer for querying data
