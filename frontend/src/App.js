//temp AI code
//the root component that holds the visual structure and logic of your user interface

import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Container, Nav, Navbar } from 'react-bootstrap';

import Home from './pages/Home';
import Search from './pages/Search';
import Upload from './pages/Upload';
import Analysis from './pages/Analysis';

function App() {
  return (
  <BrowserRouter>
    {/*NavBar*/}
    <Navbar expand="lg" className="bg-body-tertiary">
      <Container className="d-flex flex-column align-items-stretch">
        
        {/*Top Row*/}
        <div className="d-flex justify-content-between align-items-center w-100">
          <Navbar.Brand as={Link} to="/">Repertoire(Logo)</Navbar.Brand>
          
          <Navbar.Toggle aria-controls="basic-navbar-nav" />    {/*Menu formatting for smaller screens*/}

          <Nav className="d-none d-lg-flex">
            <Nav.Link as={Link} to="/Login">Login</Nav.Link>
          </Nav>
        </div>

        {/*Bottom Row*/}
        <Navbar.Collapse id="basic-navbar-nav" className="w-100">               {/*Hides navigation content on smaller screens*/}
          <Nav className="ms-auto align-items-center">
              {/* On smaller screens, include Login inside the collapsed menu */}
              <Nav.Link as={Link} to="/Login" className="d-lg-none">Login</Nav.Link>
              <Nav.Link as={Link} to="/">Home</Nav.Link>
              <Nav.Link as={Link} to="/Search">Search</Nav.Link>
              <Nav.Link as={Link} to="/Upload">Upload</Nav.Link>
              <Nav.Link as={Link} to="/Analysis">Analysis</Nav.Link>
          </Nav>
        </Navbar.Collapse>

      </Container>
    </Navbar>

    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/Search" element={<Search />} />
      <Route path="/Upload" element={<Upload />} />
      <Route path="/Analysis" element={<Analysis />} />
    </Routes>
  </BrowserRouter>
  );
}

export default App;