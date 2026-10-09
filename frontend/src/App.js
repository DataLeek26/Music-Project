//temp AI code
//the root component that holds the visual structure and logic of your user interface

import React, { useState, useEffect } from 'react';
import { Container, Card, Spinner, Alert } from 'react-bootstrap';
import Nav from 'react-bootstrap/Nav';
import Navbar from 'react-bootstrap/Navbar';

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
  <>
    {/*NavBar*/}
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container className="d-flex flex-column align-items-stretch">
        
        {/*Top Row*/}
        <div className="d-flex justify-content-between align-items-center w-100">
          <Navbar.Brand href="home">Repitoire</Navbar.Brand>
          
          <Navbar.Toggle aria-controls="basic-navbar-nav" />    {/*Menu formatting for smaller screens*/}

          <Nav className="d-none d-lg-flex">
            <Nav.Link href="login">Login</Nav.Link>
          </Nav>
        </div>

        {/*Bottom Row*/}
        <Navbar.Collapse id="basic-navbar-nav" className="w-100">               {/*Hides navigation content on smaller screens*/}
          <Nav className="ms-auto align-items-center">
              {/* On smaller screens, include Login inside the collapsed menu */}
              <Nav.Link href="login" className="d-lg-none">Login</Nav.Link>
              <Nav.Link href="home">Home</Nav.Link>
              <Nav.Link href="search">Search</Nav.Link>
              <Nav.Link href="upload">Upload</Nav.Link>
              <Nav.Link href="analysis">Analysis</Nav.Link>
          </Nav>
        </Navbar.Collapse>

      </Container>
    </Navbar>
    
    {/*Card - Connection Test*/}
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
  </>
  );
}

export default App;