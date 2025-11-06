module.exports = {
  networks: {
    development: {
      host: "127.0.0.1",     // Localhost (Ganache's default)
      port: 7545,            // Standard Ganache port
      network_id: "*",       // Match any network id
    },
  },

  // Configure your compilers
  compilers: {
    solc: {
      version: "0.8.19",    // Use a specific compiler version
    }
  },
};