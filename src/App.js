import React, { useState, useEffect } from 'react';
import Button from 'react-bootstrap/Button'
import Form from 'react-bootstrap/Form'
import './App.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import io from 'socket.io-client';

function App() {

      const [currentTime, setCurrentTime] = useState(0);

      useEffect(() => {
        fetch('/api/time').then(res => res.json()).then(data => {
          setCurrentTime(data.time);
        });
        const socket = io()
        return () => { socket.disconnect() }; // disconnect socket when page unmounts
      }, []);

      const [dropHeight, setDropHeight] = useState('')
      const [dropColumns, setDropColumns] = useState('')
      const [dropRows, setDropRows] = useState('')
      const [dropSpacing, setDropSpacing] = useState('')

      const [flightStarted, setFlightStarted] = useState(false)
      
      // Submit Flight Parameters to Backend

      function submitParams() {
        const flightParams = ({
          dropHeight: dropHeight,
          dropColumns: dropColumns,
          dropRows: dropRows,
          dropSpacing: dropSpacing
        })
        console.log(flightParams)
        if (dropHeight !== '' && dropColumns !== '' && dropRows !== '' && dropSpacing !== '') {
          fetch('/api/params', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(flightParams)
          }).then(res => console.log(res.ok))
          .then(() => setFlightStarted(true))
          .catch(err => console.log(err))
        }
        }

        // Mission Log

      const [missionLog, setMissionLog] = useState([])

      function getMissionLog() {
        fetch('/api/log', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
        }).then(res => res.json()).then(data => setMissionLog(data.missionLog))
      }
      
      const missionLogList = missionLog.map((log) => 
        <li>{log}</li>
      )

      // useEffect(() => {
      //   getMissionLog()
      // }, [missionLog])

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
        <Button onClick={submitParams} className="start-flight" variant="warning">Start Flight</Button>
        </>
        }

        {flightStarted && 
          <div>
            <h3>Mission Log</h3>
            <Button onClick={getMissionLog} className="start-flight" variant="warning">Get Mission Log</Button>
            <div className='mission-log'>
              <ul>{missionLogList}</ul>
            </div>
          </div>
          }

      </header>
    </div>
  );
}

export default App;


