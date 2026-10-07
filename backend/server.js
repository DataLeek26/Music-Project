//temp AI code

const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 5000;

// Enable CORS so React frontend on port 3000 can talk to this server
app.use(cors()); // Allows frontend to make requests from port 3000
app.use(express.json());

// Test API Endpoint
app.get('', (req, res) => {
  res.json({ message: "Hello from Node Express backend!" });
});

app.listen(PORT, () => {
  console.log('Backend server running on http://localhost:5000');
});