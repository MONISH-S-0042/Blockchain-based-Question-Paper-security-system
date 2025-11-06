// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract QuestionPaperStorage {
    struct Paper {
        string ipfsHash;
        uint256 releaseTime;
        bytes aesKey;
        address faculty;
        bool isSet;
    }

    mapping(string => Paper) public papers;
    mapping(address => bool) public authorizedUsers;
    address public owner;

    event PaperUploaded(string paperId, address indexed faculty);
    event PaperDownloaded(string paperId, address indexed downloader);
    event AccessFailed(
        string paperId,
        address indexed requester,
        string reason
    );
    event UserAuthorized(address indexed user);
    event UserRevoked(address indexed user);

    constructor() {
        owner = msg.sender;
        authorizedUsers[msg.sender] = true; 
    }

    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can perform this action.");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedUsers[msg.sender], "Not an authorized user.");
        _;
    }

    // Add authorized wallet address (student/faculty)
    function addAuthorizedUser(address _user) public onlyOwner {
        authorizedUsers[_user] = true;
        emit UserAuthorized(_user);
    }

    // Remove access for a wallet
    function revokeUser(address _user) public onlyOwner {
        authorizedUsers[_user] = false;
        emit UserRevoked(_user);
    }

    // Upload paper (only owner/faculty)
    function uploadQuestionPaper(
        string memory _paperId,
        string memory _ipfsHash,
        uint256 _releaseTime,
        bytes memory _aesKey
    ) public onlyOwner {
        require(!papers[_paperId].isSet, "Paper ID already exists.");
        require(
            _releaseTime > block.timestamp,
            "Release time must be in the future"
        );

        papers[_paperId] = Paper({
            ipfsHash: _ipfsHash,
            releaseTime: _releaseTime,
            aesKey: _aesKey,
            faculty: msg.sender,
            isSet: true
        });

        emit PaperUploaded(_paperId, msg.sender);
    }

    // Record access attempts
    function recordAccess(string memory _paperId) public onlyAuthorized {
        require(papers[_paperId].isSet, "Paper not found.");

        if (block.timestamp >= papers[_paperId].releaseTime) {
            emit PaperDownloaded(_paperId, msg.sender);
        } else {
            emit AccessFailed(_paperId, msg.sender, "Paper not yet released");
        }
    }

    // Get paper (authorized + after release)
    function getPaperDetails(
        string memory _paperId
    ) public view onlyAuthorized returns (string memory, bytes memory) {
        require(papers[_paperId].isSet, "Paper not found.");
        require(
            block.timestamp >= papers[_paperId].releaseTime,
            "Paper not yet released"
        );
        return (papers[_paperId].ipfsHash, papers[_paperId].aesKey);
    }
}
