import React, { useState } from 'react';
import Button from 'react-bootstrap/Button'
import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import io from 'socket.io-client';

function App() {

    const socket = io();

    const [flightStatus, setFlightStatus] = useState('Flight not started')
    const [count, setCount] = useState(0)

    function startFlight() {
      axios({
        method: 'get',
        url: '/flight',
      }).then(res => setFlightStatus(res.data.test))
      .catch(err => console.log(err));
      
      socket.emit("start");
    }

      socket.on('elapsed time', (data) => {
            setCount(data.count)
          })
    
    
  return (
    <div className="App">
      <header className="App-header">

        <h1>Seed Planting IoT Drone</h1>

        <div><Button onClick={startFlight} variant="warning">Start Flight</Button></div>
        <h3>{flightStatus}</h3>
        <h2>Seconds = {count}</h2>

      </header>
    </div>
  );
}

export default App;

