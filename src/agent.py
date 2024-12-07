# agent.py
import logging
import threading
from fastapi import FastAPI
from web3 import Web3
from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Connect to the Ethereum network (same as in endpoints.py)
WEB3_PROVIDER = "https://137.rpc.thirdweb.com/7e03b521d3a4923ed34206b134e43261"
CHAIN_ID = 137
CONTRACT_ADDRESS = "0x8f1c24a3c8331E642De8dBFF976bf3903fF84d5c"

# Initialize Web3 and contract (same as in endpoints.py)
web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
CONTRACT_ABI = [
        {
            "inputs": [
                {"internalType": "string", "name": "_title", "type": "string"},
                {"internalType": "string", "name": "_description", "type": "string"}
            ],
            "name": "createProposal",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"},
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "name": "createdProposals",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}],
            "name": "deleteProposal",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}],
            "name": "executeProposal",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "getAllProposals",
            "outputs": [
                {
                    "components": [
                        {"internalType": "string", "name": "title", "type": "string"},
                        {"internalType": "string", "name": "description", "type": "string"},
                        {"internalType": "uint256", "name": "voteCount", "type": "uint256"},
                        {"internalType": "bool", "name": "executed", "type": "bool"},
                        {"internalType": "address", "name": "creator", "type": "address"}
                    ],
                    "internalType": "struct VotingDAO.Proposal[]",
                    "name": "",
                    "type": "tuple[]"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}],
            "name": "getProposal",
            "outputs": [
                {"internalType": "string", "name": "title", "type": "string"},
                {"internalType": "string", "name": "description", "type": "string"},
                {"internalType": "uint256", "name": "voteCount", "type": "uint256"},
                {"internalType": "bool", "name": "executed", "type": "bool"},
                {"internalType": "address", "name": "creator", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "address", "name": "_creator", "type": "address"}],
            "name": "getProposalHistory",
            "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "address", "name": "_voter", "type": "address"}],
            "name": "getVoteHistory",
            "outputs": [{"internalType": "uint256[]", "name": "", "type": "uint256[]"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "address", "name": "", "type": "address"},
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "name": "hasVoted",
            "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [],
            "name": "proposalCount",
            "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [
                {"internalType": "uint256", "name": "", "type": "uint256"}
            ],
            "name": "proposals",
            "outputs": [
                {"internalType": "string", "name": "title", "type": "string"},
                {"internalType": "string", "name": "description", "type": "string"},
                {"internalType": "uint256", "name": "voteCount", "type": "uint256"},
                {"internalType": "bool", "name": "executed", "type": "bool"},
                {"internalType": "address", "name": "creator", "type": "address"}
            ],
            "stateMutability": "view",
            "type": "function"
        },
        {
            "inputs": [{"internalType": "uint256", "name": "_proposalId", "type": "uint256"}],
            "name": "vote",
            "outputs": [],
            "stateMutability": "nonpayable",
            "type": "function"
        }
    ]
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Caching mechanism for proposals and voting information (same as in endpoints.py)
cached_proposals = []
cached_vote_history = {}
cache_lock = threading.Lock()

def refresh_cache():
    """Fetches and caches proposals and vote history."""
    global cached_proposals
    
    with cache_lock:
        try:
            proposal_count = contract.functions.proposalCount().call()
            cached_proposals.clear()
            
            for proposal_id in range(proposal_count):
                title, description, vote_count, executed = contract.functions.getProposal(proposal_id).call()
                cached_proposals.append({
                    "proposal_id": proposal_id,
                    "title": title,
                    "description": description,
                    "vote_count": vote_count,
                    "executed": executed
                })
            logger.info("Cache refreshed successfully.")
        except Exception as e:
            logger.error(f"Failed to refresh cache: {str(e)}")

# Call refresh_cache at startup or at intervals as needed.
refresh_cache()

# Initialize OpenAI GPT model with proper configuration (same as in endpoints.py)
llm = ChatOpenAI(model_name="gpt-4", temperature=0.7)

# Define prompts for analysis and chat interactions (same as in endpoints.py)
analyze_prompt = PromptTemplate(
    input_variables=["title", "description"],
    template=(
        "You are an AI agent assisting in a decentralized autonomous organization (DAO). "
        "Analyze the following proposal and provide feedback on its clarity, potential impact, "
        "and areas of improvement.\n\n"
        "Title: {title}\n"
        "Description: {description}\n\n"
        "Your analysis:"
    ),
)

chat_prompt = PromptTemplate(
    input_variables=["message", "dao_info", "vote_history"],
    template=(
        "You are an AI assistant for a DAO voting platform. Respond conversationally to the following message, "
        "providing helpful and accurate information about the DAO, voting process, or general inquiries.\n\n"
        "DAO Information: {dao_info}\n"
        "User Vote History: {vote_history}\n"
        "User: {message}\n"
        "Assistant:"
    ),
)

# Create runnables for tasks (same as in endpoints.py)
analyze_runnable = RunnableLambda(lambda inputs: llm(analyze_prompt.format(**inputs)))
chat_runnable = RunnableLambda(lambda inputs: llm(chat_prompt.format(**inputs)))

