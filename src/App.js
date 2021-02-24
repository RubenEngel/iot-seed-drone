import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Input from './components/Input';
import Route from './images/mission_route.png'
import { BsFillChatSquareDotsFill, BsBarChartFill } from "react-icons/bs";
import MissionLog from './components/MissionLog'
import MissionStats from './components/MissionStats'

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
          .then(() => {
            socket.emit('flight-start')
            socket.emit('flight-stats')
        })
          .catch(err => console.log(err))
        } else {
          console.log('Specify all parameters')
        }
        }

      // Page
      const [page, setPage] = useState('log')

      // Flight Stats
      const [flightStats, setFlightStats] = useState({
        'altitude': null,
        'airspeed': null,
        'battery': null,
        'obstacle': null
      })
      const [col, setCol] = useState(null)
      const [row, setRow] = useState(null)

      // Mission Log
      const [missionLog, setMissionLog] = useState([])
      const missionLogList = missionLog.map((log, index) => 
        <p className='mb-6' key={index}>{log}</p>
      )

      useEffect(() => {
        fetch('/api/time').then(res => res.json()).then(data => {
          setCurrentTime(data.time); 
         });
         socket.on('message', (data) => {
          const colRegExp = new RegExp('(?<=Column: )[0-9]+')
          const rowRegExp = new RegExp('(?<=Row: )[0-9]+')
          colRegExp.exec(data) && setCol(colRegExp.exec(data)[0])
          rowRegExp.exec(data) && setRow(rowRegExp.exec(data)[0])
          setMissionLog(missionLog => [...missionLog, data])
        })
        socket.on('status', (status) => {
        if (status === 'complete') {
          setFlightStarted(false)
          setMissionLog([])
          setCol(0)
          setRow(0)
        }})
        socket.on('stats', (stats) => {
          try {
            setFlightStats(JSON.parse(stats))
          } catch (error) {
            console.log('Not valid JSON')
            return error;
          }
        })
        socket.on('progress', (data) => {
            console.log(data)
        })

        return () => {
          socket.disconnect()
        }; // disconnect sockets when page unmounts
      }, [])


  return (
    <>

        <div className='p-3'>
          {/* Page title */}
          <h1 className='text-4xl text-blue-500'>SeedGenCopter</h1>
          {/* Checks server connection by getting current time from server */}
          <h3 className=' text-base'>Server Status: {currentTime ? currentTime : 'Failed'}</h3>
        </div>

        {!flightStarted && // If the flight has not started render mission parameters page
        <>
        <div className='md:grid md:grid-cols-2 items-center max-w-5xl mx-auto'>
          {/* Image showing example mission route */}
          <div className='m-auto container max-w-lg'>
            <img src={Route} alt='Example mission route'/>
          </div>
          {/* Input boxes for flight parameters */}
          <div>
            <h2 className='text-3xl lg:text-4xl text-blue-500'>Mission Parameters</h2>
            <form className='my-3 flex flex-col place-items-center text-2xl'>
              <Input name='Height' onChange={e => setDropHeight(e.target.value)} value={dropHeight}/>
              <Input name='Columns' onChange={e => setDropColumns(e.target.value)} value={dropColumns}/>
              <Input name='Rows' onChange={e => setDropRows(e.target.value)} value={dropRows}/>
              <Input name='Spacing' onChange={e => setDropSpacing(e.target.value)} value={dropSpacing}/>
            </form>
          </div>

        </div>

        <div className='mt-6'>
            <button 
              className='text-xl md:text-2xl py-2 px-4 mb-8 border-2 rounded-lg border-green-600 hover:bg-green-600 hover:text-white' 
              onClick={submitParams}>
                Start Flight
            </button>
          </div>

        </>
        }

        { !flightStarted && 
          <>
          {page === 'log' && <MissionLog missionLogList={missionLogList}/>}
          {page === 'stats' && <MissionStats flightStats={flightStats} col={col} row={row}/>}
          
          <div className='flex flex-row text-center justify-center my-10'>
            <button onClick={() => setPage('log')} className='focus:outline-none'>
              <BsFillChatSquareDotsFill className={'text-5xl mx-10' + ((page === 'log') ? ' text-blue-500' : ' text-black')}/>
            </button>
            <button onClick={() => setPage('stats')} className={'focus:outline-none' + ((page === 'stats') ? ' text-blue-500' : ' text-black')}>
              <BsBarChartFill className='text-5xl mx-10'/>
            </button>
          </div>
          </>
          }

    </>
  );
}

export default App;
