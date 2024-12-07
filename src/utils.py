
from web3 import Web3

def initialize_web3():
    WEB3_PROVIDER = "https://137.rpc.thirdweb.com/7e03b521d3a4923ed34206b134e43261"
    CHAIN_ID = 137
    CONTRACT_ADDRESS = "0x8f1c24a3c8331E642De8dBFF976bf3903fF84d5c"
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
    
    web3 = Web3(Web3.HTTPProvider(WEB3_PROVIDER))
    contract = web3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)
    return web3, contract