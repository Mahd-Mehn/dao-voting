
# DAO Voting Platform

This project is a decentralized autonomous organization (DAO) voting platform built using **FastAPI**, **Web3.py**, and **LangChain**. It allows users to create proposals, vote on them, and interact with the DAO through a conversational AI assistant.

---

## Features

- **Create Proposals**: Submit new proposals for the DAO.
- **Vote on Proposals**: Cast votes on existing proposals.
- **View Proposals**: Retrieve all proposals and their details.
- **Check Balance**: View user balances in Ether.
- **Voting History**: Check the voting history for a specific address.
- **Proposal Analysis**: Analyze proposals for clarity and potential impact using an AI assistant.
- **AI Assistant**: Chat with an AI assistant for DAO-related queries.

---

## Project Structure

```
/dao-voting-agent
│
├── main.py      # Main application entry point, initializes FastAPI app and includes endpoints for interacting with the DAO
/dao-voting-agent/src
    ├── models.py        # Pydantic models for request and response schemas
    ├── utils.py     # utility codes
    └── agent.py         # Logic for analyzing proposals and chatting with users
```

---

## Technologies Used

- **FastAPI**: A modern web framework for building APIs with Python 3.6+ based on standard Python type hints.
- **Web3.py**: A Python library for interacting with the Ethereum blockchain.
- **LangChain**: A framework for developing applications powered by language models.

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/okoliechykwuka/dao-voting-agent.git
cd dao-voting-agent
```

### 2. Install Dependencies

* Python 3.9+

* Node.js and npm (optional, for testing contracts)

* A custom blockchain endpoint

* OpenAI API Key

Make sure you have Python 3.10+ installed, then create a virtual environment and install the required packages:

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

### 3. Configure the Smart Contract

Update the **`CONTRACT_ABI`** in `endpoints.py` with your smart contract's ABI. Ensure the following are correctly set to connect to your Ethereum network:

- **`WEB3_PROVIDER`**
- **`CONTRACT_ADDRESS`**
- **`CHAIN_ID`**

### 4. Run the Application

Start the FastAPI application using Uvicorn:

```bash
uvicorn main:app --reload
```

### 5. Access the API

**ENDPOINTS**
![Endpoints](image.png)


Open your browser and navigate to:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Usage Examples

### Create a Proposal

**Request**:  
`POST /proposals`  
**Body**:

```json
{
  "title": "Proposal Title",
  "description": "Proposal Description",
  "private_key": "your_private_key"
}
```

---

### Vote on a Proposal

**Request**:  
`POST /vote`  
**Body**:

```json
{
  "proposal_id": 1,
  "private_key": "your_private_key"
}
```

---

### Get All Proposals

**Request**:  
`GET /proposals`

---

### Get Proposal Details

**Request**:  
`GET /proposals/{proposal_id}`

---

### Get User Balance

**Request**:  
`GET /balance/{address}`

---

### Get Voting History

**Request**:  
`GET /vote_history/{address}`

---

### Chat with AI Assistant

**Request**:  
`POST /chat`  
**Body**:

```json
{
  "message": "What is the current status of proposals?",
  "user_address": "0xYourEthereumAddress"
}
```

---

### Analyze a Proposal

**Request**:  
`POST /analyze_proposal`  
**Body**:

```json
{
  "title": "Proposal Title",
  "description": "Proposal Description"
}
```
