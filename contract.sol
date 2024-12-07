// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VotingDAO {
    struct Proposal {
        string title;
        string description;
        uint256 voteCount;
        bool executed;
    }

    mapping(uint256 => Proposal) public proposals;
    uint256 public proposalCount;

    mapping(address => mapping(uint256 => bool)) public hasVoted;


    function createProposal(string memory _title, string memory _description) public {
        proposals[proposalCount] = Proposal({
            title: _title,
            description: _description,
            voteCount: 0,
            executed: false
        });
        proposalCount++;
    }


    function getProposal(uint256 _proposalId) public view returns (
        string memory title,
        string memory description,
        uint256 voteCount,
        bool executed
    ) {
        require(_proposalId < proposalCount, "Invalid proposal");
        Proposal memory proposal = proposals[_proposalId];
        return (proposal.title, proposal.description, proposal.voteCount, proposal.executed);
    }


    function getAllProposals() public view returns (Proposal[] memory) {
        Proposal[] memory allProposals = new Proposal[](proposalCount);
        for (uint256 i = 0; i < proposalCount; i++) {
            allProposals[i] = proposals[i];
        }
        return allProposals;
    }


    function vote(uint256 _proposalId) public {
        require(_proposalId < proposalCount, "Invalid proposal");
        require(!hasVoted[msg.sender][_proposalId], "Already voted");

        proposals[_proposalId].voteCount++;
        hasVoted[msg.sender][_proposalId] = true;
    }


    function deleteProposal(uint256 _proposalId) public {
        require(_proposalId < proposalCount, "Invalid proposal");
        require(proposals[_proposalId].voteCount == 0, "Cannot delete after voting has started");

        // Shift all proposals after the deleted one to fill the gap
        for (uint256 i = _proposalId; i < proposalCount - 1; i++) {
            proposals[i] = proposals[i + 1];
        }
        delete proposals[proposalCount - 1];
        proposalCount--;
    }

    function executeProposal(uint256 _proposalId) public {
        require(_proposalId < proposalCount, "Invalid proposal");
        Proposal storage proposal = proposals[_proposalId];
        require(!proposal.executed, "Proposal already executed");
        require(proposal.voteCount > 0, "Proposal must have votes");

        proposal.executed = true;
    }
}