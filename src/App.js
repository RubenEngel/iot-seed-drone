import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
// import axios from 'axios';
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
// import io from 'socket.io-client';

function App() {

    // const socket = io();

    // const [flightStatus, setFlightStatus] = useState('Flight not started')
    // const [count, setCount] = useState(0)

    // function startFlight() {
    //   axios({
    //     method: 'get',
    //     url: '/flight',
    //   }).then(res => setFlightStatus(res.data.test))
    //   .catch(err => console.log(err));
      
    //   socket.emit("start");
    // }

      // socket.on('elapsed time', (data) => {
      //       setCount(data.count)
      //     })
    
      const [currentTime, setCurrentTime] = useState(0);

      useEffect(() => {
        fetch('/api/time').then(res => res.json()).then(data => {
          setCurrentTime(data.time);
        });
      }, []);

      const [dropHeight, setDropHeight] = useState('')
      const [dropColumns, setDropColumns] = useState('')
      const [dropRows, setDropRows] = useState('')
      const [dropSpacing, setDropSpacing] = useState('')
      const [flightStarted, setFlightStarted] = useState(false)
      const [missionLog, setMissionLog] = useState([])

      function handleSubmit() {
        const flightParams = ({
          dropHeight: dropHeight,
          dropColumns: dropColumns,
          dropRows: dropRows,
          dropSpacing: dropSpacing
        })
        console.log(flightParams)
        if (dropHeight !== '' && dropColumns !== '' && dropRows !== '') {
          setFlightStarted(true)
          fetch('/api/params', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(flightParams)
          }).then(res => console.log(res.ok))
          .catch(err => console.log(err))
        }
        }

      function getMissionLog() {
        fetch('/api/log', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        }).then(res => res.json()).then(data => setMissionLog(data.missionLog))
      }
      
      const missionLogList = missionLog.map((log) => 
        <li>{log}</li>
      )


  return (
    <div className="App">
      <header className="App-header">

        <h1>Seed Planting IoT Drone</h1>
        <h3>{currentTime}</h3>

        {!flightStarted && 
        <>
        <Form>
          <Form.Label>Drop Height</Form.Label>
            <Form.Control onChange={e => setDropHeight(e.target.value)} value={dropHeight} type="number"/>
          <Form.Label>Drop Columns</Form.Label>
            <Form.Control onChange={e => setDropColumns(e.target.value)} value={dropColumns} type="number"/>
          <Form.Label>Drop Rows</Form.Label>
            <Form.Control onChange={e => setDropRows(e.target.value)} value={dropRows} type="number"/>
          <Form.Label>Drop Spacing</Form.Label>
            <Form.Control onChange={e => setDropSpacing(e.target.value)} value={dropSpacing} type="number"/>
        </Form>
        <Button onClick={handleSubmit} className="start-flight" variant="warning">Start Flight</Button>
        </>
        }

        {flightStarted && 
          <div>
            <h3>Mission Log</h3>
            <Button onClick={getMissionLog} className="start-flight" variant="warning">Get Mission Log</Button>
            <ul>{missionLogList}</ul>
          </div>
          }

      </header>
    </div>
  );
}

export default App;


