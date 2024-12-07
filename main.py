from fastapi import FastAPI, HTTPException
import logging
from web3 import Web3
from web3.exceptions import ContractLogicError
from src.model import (
    AddressRequest,
    AnalyzeProposalRequest,
    AnalyzeProposalResponse,
    BalanceResponse,
    ChatRequest,
    ChatResponse,
    CreateProposalRequest,
    DeleteProposalRequest,
    ProposalDetailRequest,
    ProposalHistoryRequest,
    ProposalHistoryResponse,
    ProposalResponse,
    TransactionResponse,
    VoteRequest,
    VoteHistoryRequest,
    VoteHistoryResponse
)
from src.utils import initialize_web3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()
CHAIN_ID = 137

# Initialize Web3 and contract
web3, contract = initialize_web3()

def sign_and_send_transaction(tx, private_key):
    try:
        signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
        tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        return tx_hash.hex()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")


@app.get("/proposals", summary="Get All Proposals")
async def get_all_proposals():
    """
    Retrieve a list of all proposals stored in the contract.
    """
    try:
        proposals_data = contract.functions.getAllProposals().call()
        proposals = []
        for i, p in enumerate(proposals_data):
            # p = (title, description, voteCount, executed, creator)
            proposals.append({
                "proposal_id": i,
                "title": p[0],
                "description": p[1],
                "vote_count": p[2],
                "executed": p[3],
                "creator": p[4]
            })
        return {"proposals": proposals}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/proposals", response_model=TransactionResponse, summary="Create Proposal")
async def create_proposal(request: CreateProposalRequest):
    """
    Create a new proposal by providing a title, description, and the creator's private key.
    """
    account = web3.eth.account.from_key(request.private_key)
    gas_price = web3.to_wei('50', 'gwei')

    tx = contract.functions.createProposal(request.title, request.description).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 2000000,
        "gasPrice": gas_price,
        "chainId": CHAIN_ID,
    })

    tx_hash = sign_and_send_transaction(tx, request.private_key)
    return {"transaction_hash": tx_hash}


@app.post("/vote", response_model=TransactionResponse, summary="Vote On Proposal")
async def vote_on_proposal(request: VoteRequest):
    """
    Vote on a specific proposal by providing the proposal ID and the voter's private key.
    """
    account = web3.eth.account.from_key(request.private_key)
    gas_price = web3.to_wei('1', 'gwei')

    tx = contract.functions.vote(request.proposal_id).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 2000000,
        "gasPrice": gas_price,
        "chainId": web3.eth.chain_id,
    })

    tx_hash = sign_and_send_transaction(tx, request.private_key)
    return {"transaction_hash": tx_hash}


@app.post("/proposals/detail", summary="Get Proposal")
async def get_proposal_detail(request: ProposalDetailRequest):
    """
    Retrieve details for a specific proposal by its ID.
    """
    try:
        title, description, vote_count, executed, creator = contract.functions.getProposal(request.proposal_id).call()
        return {
            "proposal_id": request.proposal_id,
            "title": title,
            "description": description,
            "vote_count": vote_count,
            "executed": executed,
            "creator": creator
        }
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/balance", response_model=BalanceResponse, summary="Get Balance")
async def get_balance(request: AddressRequest):
    """
    Retrieve the ETH balance of a given address.
    """
    try:
        address = Web3.to_checksum_address(request.address)
        balance_wei = web3.eth.get_balance(address)
        balance_ether = web3.fromWei(balance_wei, 'ether')
        return {"balance": str(balance_ether)}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid Ethereum address")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/vote_history", response_model=VoteHistoryResponse, summary="Get Vote History")
async def get_vote_history(request: VoteHistoryRequest):
    """
    Retrieve the history of proposal IDs that a given address has voted on.
    """
    try:
        address = Web3.to_checksum_address(request.address)
        proposal_ids = contract.functions.getVoteHistory(address).call()
        return {"voter": request.address, "voted_proposal_ids": proposal_ids}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/proposal_history", response_model=ProposalHistoryResponse, summary="Get Proposal History")
async def get_proposal_history(request: ProposalHistoryRequest):
    """
    Retrieve the history of proposal IDs created by a specific address.
    """
    try:
        address = Web3.to_checksum_address(request.address)
        proposal_ids = contract.functions.getProposalHistory(address).call()
        return {"creator": request.address, "proposal_ids": proposal_ids}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/proposals/{proposal_id}", response_model=TransactionResponse, summary="Delete Proposal")
async def delete_proposal(proposal_id: int, request: DeleteProposalRequest):
    """
    Delete a proposal by its ID. The requester must be the proposal creator.
    """
    if proposal_id != request.proposal_id:
        raise HTTPException(status_code=400, detail="Mismatch in proposal_id between path and body")

    account = web3.eth.account.from_key(request.private_key)
    gas_price = web3.to_wei('1', 'gwei')

    try:
        tx = contract.functions.deleteProposal(proposal_id).build_transaction({
            "from": account.address,
            "nonce": web3.eth.get_transaction_count(account.address),
            "gas": 2000000,
            "gasPrice": gas_price,
            "chainId": web3.eth.chain_id,
        })

        tx_hash = sign_and_send_transaction(tx, request.private_key)
        return {"transaction_hash": tx_hash}
    except ContractLogicError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception:
        raise HTTPException(status_code=500, detail="Internal server error")


@app.post("/analyze_proposal", response_model=AnalyzeProposalResponse, summary="Analyze Proposal")
async def analyze_proposal(request: AnalyzeProposalRequest):
    """
    Analyze a proposal's title and description using a custom agent.
    """
    from src.agent import analyze_runnable
    try:
        analysis = await analyze_runnable.invoke({"title": request.title, "description": request.description})
        return AnalyzeProposalResponse(analysis=analysis)
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")


@app.post("/chat", response_model=ChatResponse, summary="Chat")
async def chat(request: ChatRequest):
    """
    Chat endpoint that uses a custom agent to respond to user messages with DAO context.
    """
    from src.agent import chat_runnable, cached_proposals, cached_vote_history
    try:
        # Prepare DAO information from cache
        dao_info = f"The DAO currently has {len(cached_proposals)} proposals."

        # Fetch user's voting history from cache (if available)
        vote_history = cached_vote_history.get(request.user_address, [])

        reply = await chat_runnable.invoke({"message": request.message, "dao_info": dao_info, "vote_history": vote_history})
        return ChatResponse(reply=reply)
    except Exception as e:
        logger.error(f"Chat failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")
