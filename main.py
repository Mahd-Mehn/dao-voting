from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from web3 import Web3

app = FastAPI()

# Connect to the custom chain RPC URL
WEB3_PROVIDER = "https://5165.rpc.thirdweb.com/7e03b521d3a4923ed34206b134e43261"
CHAIN_ID = 5165  # Your custom chain's ID
CONTRACT_ADDRESS = "0x29192C5d95BF89B8Db9e4390Bb175b811277b005"
CONTRACT_ABI = [{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"createProposal","inputs":[{"type":"string","name":"_title","internalType":"string"},{"type":"string","name":"_description","internalType":"string"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"deleteProposal","inputs":[{"type":"uint256","name":"_proposalId","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"executeProposal","inputs":[{"type":"uint256","name":"_proposalId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"tuple[]","name":"","internalType":"struct VotingDAO.Proposal[]","components":[{"type":"string","name":"title","internalType":"string"},{"type":"string","name":"description","internalType":"string"},{"type":"uint256","name":"voteCount","internalType":"uint256"},{"type":"bool","name":"executed","internalType":"bool"}]}],"name":"getAllProposals","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"title","internalType":"string"},{"type":"string","name":"description","internalType":"string"},{"type":"uint256","name":"voteCount","internalType":"uint256"},{"type":"bool","name":"executed","internalType":"bool"}],"name":"getProposal","inputs":[{"type":"uint256","name":"_proposalId","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"bool","name":"","internalType":"bool"}],"name":"hasVoted","inputs":[{"type":"address","name":"","internalType":"address"},{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"view","outputs":[{"type":"uint256","name":"","internalType":"uint256"}],"name":"proposalCount","inputs":[]},{"type":"function","stateMutability":"view","outputs":[{"type":"string","name":"title","internalType":"string"},{"type":"string","name":"description","internalType":"string"},{"type":"uint256","name":"voteCount","internalType":"uint256"},{"type":"bool","name":"executed","internalType":"bool"}],"name":"proposals","inputs":[{"type":"uint256","name":"","internalType":"uint256"}]},{"type":"function","stateMutability":"nonpayable","outputs":[],"name":"vote","inputs":[{"type":"uint256","name":"_proposalId","internalType":"uint256"}]}]

web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# Models
class CreateProposalRequest(BaseModel):
    title: str
    description: str
    private_key: str

class VoteRequest(BaseModel):
    proposal_id: int
    private_key: str

class TransactionResponse(BaseModel):
    transaction_hash: str


# Helper function to sign and send transactions
def sign_and_send_transaction(tx, private_key):
    signed_tx = web3.eth.account.sign_transaction(tx, private_key=private_key)
    tx_hash = web3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()


# Endpoints
@app.post("/proposals", response_model=TransactionResponse)
async def create_proposal(request: CreateProposalRequest):
    account = web3.eth.account.from_key(request.private_key)
    gas_price = web3.to_wei('1', 'gwei')  # Adjust based on your chain's requirements

    tx = contract.functions.createProposal(request.title, request.description).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 2000000,
        "gasPrice": gas_price,
        "chainId": CHAIN_ID,
    })

    tx_hash = sign_and_send_transaction(tx, request.private_key)
    return {"transaction_hash": tx_hash}


@app.post("/vote", response_model=TransactionResponse)
async def vote_on_proposal(request: VoteRequest):
    account = web3.eth.account.from_key(request.private_key)
    gas_price = web3.to_wei('1', 'gwei')

    tx = contract.functions.vote(request.proposal_id).build_transaction({
        "from": account.address,
        "nonce": web3.eth.get_transaction_count(account.address),
        "gas": 2000000,
        "gasPrice": gas_price,
        "chainId": CHAIN_ID,
    })

    tx_hash = sign_and_send_transaction(tx, request.private_key)
    return {"transaction_hash": tx_hash}

@app.get("/proposals")
async def get_all_proposals():
    try:
        proposal_count = contract.functions.proposalCount().call()  # Fetch total proposal count
        proposals = []

        for proposal_id in range(proposal_count):
            # Fetch each proposal's details
            title, description, vote_count, executed = contract.functions.getProposal(proposal_id).call()
            proposals.append({
                "proposal_id": proposal_id,
                "title": title,
                "description": description,
                "vote_count": vote_count,
                "executed": executed
            })

        return {"proposals": proposals}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/proposals/{proposal_id}")
async def get_proposal(proposal_id: int):
    try:
        # Fetch details for a specific proposal
        title, description, vote_count, executed = contract.functions.getProposal(proposal_id).call()
        return {
            "proposal_id": proposal_id,
            "title": title,
            "description": description,
            "vote_count": vote_count,
            "executed": executed
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
