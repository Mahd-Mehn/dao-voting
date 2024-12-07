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

    // New function to get vote history for a specific address
    function getVoteHistory(address _voter) public view returns (uint256[] memory) {
        uint256[] memory votedProposals = new uint256[](proposalCount);
        uint256 count = 0;

        for (uint256 i = 0; i < proposalCount; i++) {
            if (hasVoted[_voter][i]) {
                votedProposals[count] = i;
                count++;
            }
        }

        // Resize the array to the correct length
        uint256[] memory result = new uint256[](count);
        for (uint256 i = 0; i < count; i++) {
            result[i] = votedProposals[i];
        }

        return result;
    }

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

        proposals[_proposalId] = Proposal({
            title: "",
            description: "",
            voteCount: 0,
            executed: false
        });
    }

    function executeProposal(uint256 _proposalId) public {
        require(_proposalId < proposalCount, "Invalid proposal");
        Proposal storage proposal = proposals[_proposalId];
        require(!proposal.executed, "Proposal already executed");
        require(proposal.voteCount > 0, "Proposal must have votes");

        proposal.executed = true;
    }
}

