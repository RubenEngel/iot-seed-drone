import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Input from './components/Input';
import Route from './images/mission_route.png'

const socket = io(); // Don't put inside App component

function App() {
      
      const [currentTime, setCurrentTime] = useState();
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
        if (dropHeight !== '' && dropColumns !== '' && dropRows !== '' && dropSpacing !== '') {
          fetch('/api/params', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(flightParams)
          }).then(res => console.log(res.ok))
          .then(() => setFlightStarted(true))
          .then(() => socket.emit('flight-start'))
          .catch(err => console.log(err))
        } else {
          console.log('Specify all parameters')
        }
        }

        // Mission Log
      const [missionLog, setMissionLog] = useState([])
      const missionLogList = missionLog.map((log, index) => 
        <li key={index}>{log}</li>
      )

      useEffect(() => {
        fetch('/api/time').then(res => res.json()).then(data => {
          setCurrentTime(data.time); 
         });
         socket.on('message', (data) => {
          setMissionLog(missionLog => [...missionLog, data])
        })
        socket.on('status', (status) => {
        if (status === 'complete') {
          setFlightStarted(false)
          setMissionLog([])
        }})
        return () => {
          socket.disconnect()
        }; // disconnect sockets when page unmounts
      }, [])


  return (
    <div>

        <div className='p-3'>
          <h1>SeedGenCopter</h1>
          <h3>Server Connected: {currentTime ? currentTime : 'Failed'}</h3>
        </div>

        {!flightStarted && 
        <div className=''>
          
          <div className='m-auto container'>
            <img src={Route} alt='Example mission route'/>
          </div>

          <div className='mt-6'>
            <h2 className='text-3xl'>Mission Parameters</h2>
          </div>
          
          <div>
            <form className='my-3 flex flex-col place-items-center text-2xl'>
              <Input name='Height' onChange={e => setDropHeight(e.target.value)} value={dropHeight}/>
              <Input name='Columns' onChange={e => setDropColumns(e.target.value)} value={dropColumns}/>
              <Input name='Rows' onChange={e => setDropRows(e.target.value)} value={dropRows}/>
              <Input name='Spacing' onChange={e => setDropSpacing(e.target.value)} value={dropSpacing}/>
            </form>
          </div>

          <div>
            <button 
              className='py-2 px-4 border-2 rounded-lg border-green-600 hover:bg-green-600 hover:text-white' 
              onClick={submitParams}>
                Start Flight
            </button>
          </div>

        </div>
        }

        {flightStarted && 
          
          <div>
            <h3>Mission Log</h3>
            <div className='mission-log'>
              <ul>{missionLogList}</ul>
            </div>
          </div>

          }

    </div>
  );
}

export default App;
