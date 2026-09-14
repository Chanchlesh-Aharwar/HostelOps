# HostelOps

An AI-powered operations manager for PG and hostel owners.

## Tech Stack

- **Backend**: Python + FastAPI
- **Frontend**: React + TypeScript + Tailwind CSS
- **Database**: MySQL 8+
- **AI Agent**: Strands Agents SDK + Amazon Bedrock
- **LLM**: Claude Sonnet via Bedrock

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

## Environment

Copy `.env.example` to `.env` and fill in your credentials.

## Database

The MySQL database `hostelops_db` should already exist with all 13 tables.
Run `database/seed_data.py` to populate sample data.
