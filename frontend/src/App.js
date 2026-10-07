//temp AI code
//the root component that holds the visual structure and logic of your user interface

import React, { useState, useEffect } from 'react';
import { Container, Card, Spinner, Alert } from 'react-bootstrap';

function App() {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetch('http://localhost:5000')
      .then((res) => {
        if (!res.ok) throw new Error('Network response failed');
        return res.json();
      })
      .then((data) => {
        setMessage(data.message);
        setLoading(false);
      })
      .catch((err) => {
        console.error('Fetch error:', err);
        setError(true);
        setLoading(false);
      });
  }, []);

  return (
    <Container className="mt-5">
      <Card className="text-center p-4 shadow-sm">
        <Card.Body>
          <Card.Title className="mb-4">Full-Stack Connection Test</Card.Title>

          {loading && (
            <div>
              <Spinner animation="border" variant="primary" />
              <p className="mt-2 text-muted">Connecting to Node.js backend...</p>
            </div>
          )}

          {error && (
            <Alert variant="danger">
              Failed to connect to backend! Make sure your Node.js server is running on port 5000.
            </Alert>
          )}

          {!loading && !error && (
            <Alert variant="success">
              <strong>Success!</strong> {message}
            </Alert>
          )}
        </Card.Body>
      </Card>
    </Container>
  );
}

export default App;