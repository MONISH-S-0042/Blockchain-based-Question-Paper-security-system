// Find the contract artifact that Truffle compiled
const QuestionPaperStorage = artifacts.require("QuestionPaperStorage");

// Define the deployment function
module.exports = function (deployer) {
  // Tell the deployer to deploy our contract
  deployer.deploy(QuestionPaperStorage);
};