# 🏠 HostelOps

> **AI-powered operations manager for PG and hostel owners**

HostelOps is an AI agent that helps PG and hostel owners handle repetitive day-to-day operations such as tenant complaints, maintenance coordination, vendor discovery, quote comparison, approvals, notifications, and operational activity logging.

Instead of acting as a simple chatbot, HostelOps uses an agentic workflow to understand a request, choose the appropriate tools, interact with operational data, take actions, and involve the hostel owner when human approval is required.

---

## 🎯 Problem

PG and hostel owners often manage dozens or hundreds of tenants while handling operational tasks manually:

- Maintenance complaints arrive through scattered messages.
- Owners spend time identifying rooms and tenants.
- Finding and comparing local vendors is repetitive.
- Maintenance jobs need follow-up.
- Important actions may require owner approval.
- Operational history is difficult to track consistently.

These tasks are repetitive, time-consuming, and easy to lose track of.

## 💡 Solution

**HostelOps acts as an AI operations manager.**

A hostel owner can give the agent a natural-language request such as:

> "Room 12 ka tap leak ho raha hai. Rahul tenant hai."

The agent can then:

1. Understand and classify the request.
2. Identify the relevant tenant and room.
3. Create a maintenance complaint.
4. Search suitable vendors.
5. Compare available vendor options/quotes.
6. Recommend an option.
7. Request human approval when required.
8. Create the maintenance job after approval.
9. Notify the tenant.
10. Record the completed actions for operational visibility.

This turns a natural-language request into an end-to-end operational workflow.

---

## 🤖 Why HostelOps Is Agentic

HostelOps is designed around an **AI agent + tools** architecture rather than a fixed chatbot flow.

The agent can:

- Reason about the user's request.
- Decide which tool to use.
- Retrieve information from the application.
- Create and update operational records.
- Compare vendor options.
- Decide when human approval is needed.
- Continue the workflow after approval.
- Produce an action history/audit trail.

### Example

```text
Tenant Request
      │
      ▼
Strands Agent
      │
      ▼
Understand Intent
      │
      ├───────────────┐
      ▼               ▼
Tenant/Room Tools   Complaint Tools
      │               │
      └───────┬───────┘
              ▼
        Vendor Tools
              │
              ▼
       Compare Options
              │
              ▼
       Human Approval
              │
              ▼
     Maintenance Job
              │
              ▼
      Tenant Notification
              │
              ▼
         Action Log
```

---

## ✨ Key Features

### 🏠 Hostel Operations
- Room and occupancy management
- Tenant information
- Complaint tracking
- Maintenance workflow
- Vendor management

### 🤖 AI Agent
- Natural-language operational requests
- Tool-based reasoning and execution
- Complaint classification
- Vendor discovery and comparison
- Multi-step workflow orchestration

### 👤 Human-in-the-Loop
For consequential actions, HostelOps can pause and request owner approval before execution.

### 🔔 Notifications
The workflow can notify the relevant tenant after an operational action.

### 📋 Activity & Audit Trail
Agent actions can be logged so owners can understand what happened during an automated workflow.

---

## 🏗️ Architecture

```text
┌─────────────────────────────┐
│       React Frontend        │
│     HostelOps Dashboard     │
└──────────────┬──────────────┘
               │ REST API
               ▼
┌─────────────────────────────┐
│       FastAPI Backend       │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│    Strands Agent Layer      │
│       Orchestrator          │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│       Amazon Bedrock        │
│       Foundation Model      │
└──────────────┬──────────────┘
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
   Tenant    Room    Complaint
    Tools    Tools      Tools
       │       │        │
       └───────┼────────┘
               ▼
        Vendor / Finance /
        Notification /
        Approval Tools
               │
               ▼
┌─────────────────────────────┐
│          MySQL              │
│    Operational Database     │
└─────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript |
| Backend | Python + FastAPI |
| Agent Framework | Strands Agents SDK |
| Foundation Model | Amazon Bedrock |
| Database | MySQL |
| API Style | REST |
| Cloud Platform | AWS |
| Source Control | Git + GitHub |

---

## 🔄 Core Agent Workflow

```text
1. User submits a request
        ↓
2. FastAPI receives the request
        ↓
3. Strands Agent interprets the request
        ↓
4. Agent selects required tools
        ↓
5. Tools retrieve/update application data
        ↓
6. Agent evaluates the result
        ↓
7. Additional tools are called if necessary
        ↓
8. Human approval is requested when required
        ↓
9. Approved action is executed
        ↓
10. Tenant/owner is notified
        ↓
11. Action is logged
```

---

## 📂 Project Structure

```text
hostelops/
│
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   ├── api/
│   │   ├── database/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── tools/
│   │
│   ├── tests/
│   └── requirements.txt
│
├── frontend/
│   └── src/
│
├── database/
│   ├── schema.sql
│   └── seed.sql
│
├── architecture.png
├── .env.example
├── .gitignore
├── LICENSE
└── README.md
```

> The exact folder structure may vary slightly depending on the current implementation.

---

## 🚀 Getting Started

### Prerequisites

Make sure the following are installed:

- Python 3.11+
- Node.js
- npm
- MySQL
- AWS account
- Access to the Amazon Bedrock model used by the application

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/hostelops.git
cd hostelops
```

### 2. Configure the backend

```bash
cd backend
python -m venv .venv
```

#### Windows

```powershell
.venv\Scripts\activate
```

#### macOS/Linux

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Copy the example environment file:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Fill in the required database and AWS configuration.

**Never commit `.env` or AWS credentials to GitHub.**

### 4. Set up MySQL

Create the database and run the SQL files included in the repository:

```text
database/schema.sql
database/seed.sql
```

Update the database connection settings in `.env`.

### 5. Configure Amazon Bedrock

Configure AWS credentials using a secure AWS-supported method and ensure the required Bedrock model access/permissions are available in the selected AWS Region.

Do not hard-code AWS access keys in source code.

### 6. Start the FastAPI backend

From `backend/`:

```bash
uvicorn app.main:app --reload
```

The API should be available at:

```text
http://127.0.0.1:8000
```

FastAPI documentation is normally available at:

```text
http://127.0.0.1:8000/docs
```

### 7. Start the frontend

From `frontend/`:

```bash
npm install
npm run dev
```

Open the local URL displayed by the frontend development server.

---

## 🧪 Demo Scenario

Use this scenario to demonstrate the end-to-end agent workflow:

### User request

```text
Room 12 ka tap leak ho raha hai. Rahul tenant hai.
```

### Expected workflow

```text
✓ Identify Rahul
✓ Identify Room 12
✓ Create complaint
✓ Classify as plumbing/maintenance
✓ Search available vendors
✓ Compare vendor options
✓ Recommend a vendor
✓ Request owner approval
✓ Create maintenance job after approval
✓ Notify tenant
✓ Log agent actions
```

The important point is that the agent is not merely generating a textual answer—it is coordinating actions through application tools.

---

## 🔐 Human-in-the-Loop

HostelOps is designed so that automation does not mean removing the owner from important decisions.

For actions that may create a financial or operational commitment, the system can request approval before proceeding.

```text
AI Recommendation
       ↓
Owner Approval
   ↙       ↘
Approve    Reject
   ↓
Execute     Stop
```

This creates a balance between **autonomous execution** and **human control**.

---

## 📊 Impact

HostelOps targets a practical operational problem faced by small PG and hostel businesses.

Potential benefits include:

- Less repetitive administrative work.
- Faster complaint handling.
- More structured vendor coordination.
- Better visibility into maintenance operations.
- Consistent operational records.
- Human oversight for important actions.

The long-term vision is to give small hostel operators an AI operations team without requiring them to hire a large administrative staff.

---

## 🔮 Future Roadmap

Possible future extensions include:

- WhatsApp-based tenant interaction.
- Image-based maintenance issue understanding.
- Automated rent follow-ups.
- Voice-based operational requests.
- Vendor communication and scheduling.
- Advanced analytics and operational forecasting.
- AWS production deployment.
- Agent observability and production hardening.

---

## 🧑‍💻 Development Disclosure

HostelOps was developed for the **Agents for Humans Hackathon**.

The project uses open-source frameworks and libraries including React, FastAPI, MySQL and the Strands Agents SDK.

AI coding assistants may have been used during development for implementation assistance, debugging and documentation.

Any third-party components are subject to their respective licenses and terms.

---

## 🏆 Hackathon

Built for the **Agents for Humans Hackathon** by Amazon Web Services.

### Project
**HostelOps — AI Operations Manager**

### Track
**Professional Agents**

### Core AWS Technology
**Amazon Bedrock**

### Agent Framework
**Strands Agents SDK**

---

## 📄 License

This project is licensed under the **MIT License**.

See [`LICENSE`](./LICENSE) for the complete license text.

---

## 🙌 Acknowledgements

- Amazon Web Services
- Strands Agents SDK
- Amazon Bedrock
- React
- FastAPI
- MySQL
