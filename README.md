# Repertoire Intelligence Platform

## Brief Project Statement
The College of Music hosts hundreds of performances every semester, with a vast range of genres and instruments represented in the compositions. With this wide range, it can be difficult to create accurate concert programs in an efficient manner. Because of this, the College of Music pitched a Repertoire Intelligence System to improve the accuracy and efficiency of concert program creation. 
The Repertoire Intelligence Platform will extract information about works, composers, and performers into a structured database, allowing for the use of search tools, authority control for names and titles, reporting and analytics, and AI-assisted extraction and validation workflows. 

## First time Front/Backend Install
In the terminal, open both the frontend/backend folder, and run npm install.

Troubleshooting encountered: In the folders run...

backend:
- npm install cors

frontend:
- npm install react-bootstrap bootstrap
- npm install react-router-dom

## Instructions to run Front/Backend
Enter two terminals, one in the frontend folder and another in the backend folder. Once in the folders, run...

backend: 
- node server.js
- open http://localhost:5000

frontend: 
- npm start 
- http://localhost:3000 (should automatically open)