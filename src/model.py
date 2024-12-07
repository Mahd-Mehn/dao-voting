from pydantic import BaseModel
from typing import List

# Models for proposals and related actions
class CreateProposalRequest(BaseModel):
    title: str
    description: str
    private_key: str

class ProposalRequest(BaseModel):
    proposal_id: int

class ProposalDetailRequest(BaseModel):
    proposal_id: int

class DeleteProposalRequest(BaseModel):
    proposal_id: int
    private_key: str

class AddressRequest(BaseModel):
    address: str

class VoteRequest(BaseModel):
    proposal_id: int
    private_key: str

class TransactionResponse(BaseModel):
    transaction_hash: str

class BalanceResponse(BaseModel):
    balance: str  # Using string to store balance as returned by fromWei conversion

class ProposalResponse(BaseModel):
    proposal_id: int
    title: str
    description: str
    vote_count: int
    executed: bool

class AllProposalsResponse(BaseModel):
    proposals: List[ProposalResponse]

# History requests and responses
class VoteHistoryRequest(BaseModel):
    address: str

class VoteHistoryResponse(BaseModel):
    voter: str
    voted_proposal_ids: List[int]

class ProposalHistoryRequest(BaseModel):
    address: str

class ProposalHistoryResponse(BaseModel):
    creator: str
    proposal_ids: List[int]

################  AGENT MODELS #######################
class AnalyzeProposalRequest(BaseModel):
    title: str
    description: str

class AnalyzeProposalResponse(BaseModel):
    analysis: str

class ChatRequest(BaseModel):
    message: str
    user_address: str  # User's Ethereum address for context

class ChatResponse(BaseModel):
    reply: str
