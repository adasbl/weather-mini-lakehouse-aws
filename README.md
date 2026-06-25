# Weather Mini Lakehouse on AWS

An end-to-end weather data lakehouse built on AWS. The project demonstrates data ingestion from an external API, cloud-based storage in Amazon S3, data transformation workflows, and the preparation of analytics-ready datasets following modern data engineering practices.

## Project Goal

The objective of this project is to demonstrate a simple end-to-end data pipeline that:

* Extracts weather data from a REST API
* Stores raw data in Amazon S3
* Transforms and cleans the data
* Produces analytics-ready datasets
* Follows basic data lakehouse principles

## Architecture

```text
Weather API
     │
     ▼
Ingestion Layer
     │
     ▼
Amazon S3 (Raw Data)
     │
     ▼
Transformation Layer
     │
     ▼
Curated Dataset
     │
     ▼
Analytics Layer
```

## Project Structure

```text
weather-mini-lakehouse-aws/
├── config/
│   └── stations_config.json
├── docs/
├── notebooks/
├── sql/
├── src/
│   ├── ingestion.py
│   ├── transformation.py
│   └── analytics.py
├── .env.example
├── .gitignore
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

### 1. Data Ingestion

Fetch weather data from the API and store it in Amazon S3.

```bash
python src/ingestion.py
```

### 2. Data Transformation

Clean and transform raw weather data into an analytics-ready format.

```bash
python src/transformation.py
```

### 3. Analytics

Run analytical queries and generate summary statistics.

```bash
python src/analytics.py
```

## Technologies

* Python
* Pandas
* Requests
* Boto3
* Amazon S3

## Future Improvements

* Automated orchestration with Apache Airflow
* Infrastructure as Code (Terraform)
* Data quality validation
* Incremental loading strategy
* Data catalog and metadata management
* Dashboarding with Amazon QuickSight or Power BI
