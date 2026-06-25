# Weather Mini Lakehouse on AWS

An end-to-end weather data lakehouse built on AWS. The project demonstrates data ingestion from an external API, cloud-based storage in Amazon S3, data transformation workflows, and the preparation of analytics-ready datasets following modern data engineering practices.

## Project Goal

The objective of this project is to demonstrate a simple end-to-end data pipeline that:

* Extracts weather data from a REST API
* Stores raw data in Amazon S3
* Transforms and cleans the data
* Produces analytics-ready datasets
* Follows basic data lakehouse principles

## Medallion Architecture

| Layer | Purpose | Format |
|---------|---------|---------|
| Bronze | Raw weather observations | JSON |
| Silver | Cleaned and validated datasets | Parquet |
| Gold | Analytical aggregations and reporting datasets | Parquet / Athena Tables |

## Project Structure

```text
weather-mini-lakehouse-aws/
├── config/
│   └── stations_config.json
├── docs/
├── notebooks/
├── sql/
│   ├── analytical_queries.sql
│   └── create_gold_tables.sql
├── src/
│   ├── ingestion.py
│   ├── transformation.py
│   └── analytics.py
├── .env.example
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Prerequisites

* Python 3.11+
* AWS Account or AWS Academy Lab
* Amazon S3 bucket
* Weather API access token

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd weather-mini-lakehouse-aws
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

**Linux / macOS**

```bash
source .venv/bin/activate
```

**Windows**

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a local environment file:

```bash
cp .env.example .env
```

Fill in the required values in `.env`:

```env
WEATHER_API_TOKEN=
AWS_BUCKET_NAME=
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
AWS_SESSION_TOKEN=
```

## Running the Pipeline

### 1. Bronze Layer - Data Ingestion

Fetch weather data from the external API and store raw JSON files in Amazon S3.

```bash
python src/ingestion.py
```

### 2. Silver Layer - Data Transformation

Clean and transform raw weather data into an analytics-ready format.

```bash
python src/transformation.py
```

### 3. Data Catalog Registration

Use AWS Glue Crawlers to automatically discover schemas and register Silver datasets in the Glue Data Catalog.

### 4. Gold Layer - Analytical Aggregations

Amazon Athena is used to generate analytical datasets from Silver-layer data.

The Gold layer contains aggregates such as:
- Daily weather summaries
- Temperature statistics
- Wind and precipitation metrics
- Weather anomaly detection datasets

Execute:

```sql
sql/create_gold_tables.sql
```
to create Athena CTAS tables and materialize Gold-layer datasets in: 
```text
s3://<bucket-name>/gold/
```

## Technologies

- **Python 3.11+** – data pipeline implementation
- **Pandas** – data processing and transformation
- **PyArrow** – Parquet file generation
- **Boto3** – AWS SDK for Python
- **Amazon S3** – cloud object storage (Bronze / Silver / Gold)
- **AWS Glue Data Catalog** – metadata management and schema discovery
- **Amazon Athena** – serverless SQL analytics engine