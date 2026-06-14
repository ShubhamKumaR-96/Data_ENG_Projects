# AdPulse Analytics Pipeline

A production-ready data engineering pipeline built with Apache PySpark
to analyze large-scale marketing campaign events across multiple dimensions.

## Problem Statement
A marketing platform generates 100s of GBs of ad event data daily
(impressions, clicks, video ads). This pipeline processes and analyzes
this data by joining campaign events with user profiles and store
location data to generate actionable insights.

## Architecture
Raw JSON (Local/HDFS)
↓
PySpark Processing Layer
↓
Analytical JSON Output
## Tech Stack
- Apache Spark 3.5.5 (PySpark)
- Jupyter Lab
- Docker (1 Master + 2 Workers)
- Python 3.x

## Dataset
| Dataset | Scale | Description |
|---------|-------|-------------|
| ad_campaigns_data | 100s GB/day | Ad events — impressions, clicks, video ads |
| user_profile_data | 100s GB | User demographics — gender, age, category |
| store_data | 100s MB | Store and location mapping |

## Analysis
| Question | Dimension | Description |
|----------|-----------|-------------|
| Q1 | OS Type | Event counts per campaign by operating system |
| Q2 | Store Name | Event counts per campaign by store location |
| Q3 | Gender | Event counts per campaign by user gender |

## Project Structure
adpulse-analytics-pipeline/
│
├── docker-compose.yml        # Spark cluster setup
├── datasets/                 # Raw input data
│   ├── ad_campaigns_data.jsonl
│   ├── user_profile_data.jsonl
│   └── store_data.jsonl
│
└── notebooks/
└── adpulse_analytics.ipynb  # Main analysis notebook

## Quick Start

### Prerequisites
- Docker Desktop installed

### Run
```bash
# Clone karo
git clone 
cd adpulse-analytics-pipeline

# Start karo
docker compose up -d

# Jupyter open karo
http://localhost:8888
# Token: spark123
```

### Spark UI
Spark Master : http://localhost:8080
Spark App UI : http://localhost:4040
## Sample Output
```json
{
  "campaign_id": "ABCDFAE",
  "date": "2018-10-12",
  "hour": "13",
  "type": "os_type",
  "value": "android",
  "event": {
    "impression": 1,
    "click": 1,
    "video ad": 1
  }
}
```

## Key Engineering Concepts
- NDJSON format for Spark compatibility
- DataFrame API for distributed processing
- Array explode for store place_ids join
- map_from_entries for nested event aggregation
- Modular transformation logic
