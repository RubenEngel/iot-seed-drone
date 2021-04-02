import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Input from './components/Input';
import Route from './images/mission_route.png'
import { BsFillChatSquareDotsFill, BsBarChartFill } from "react-icons/bs";
import { AiFillControl } from 'react-icons/ai'
import MissionLog from './components/MissionLog'
import MissionStats from './components/MissionStats'
// import MissionSetup from './components/MissionSetup'
import MissionFunctions from './components/MissionFunctions';
import PageContext from './page-context'

// defines a websockets instance
const socket = io();

function App() {

      // state of current time 
      const [currentTime, setCurrentTime] = useState();

      // state of user input drop height
      const [dropHeight, setDropHeight] = useState('')
      // state of user input drop columns
      const [dropColumns, setDropColumns] = useState('')
      // state of user input drop rows
      const [dropRows, setDropRows] = useState('')
      // state of user input drop spacing
      const [dropSpacing, setDropSpacing] = useState('')

      
      // Submit Flight Parameters to Backend
      function submitParams() {
        // create an object of flight parameters from user submitted values
        const flightParams = ({
          dropHeight: dropHeight,
          dropColumns: dropColumns,
          dropRows: dropRows,
          dropSpacing: dropSpacing
        })
        // if all user inputs are filled in
        if (dropHeight !== '' && dropColumns !== '' && dropRows !== '' && dropSpacing !== '') {
          // send JSON object of flight parameters to backend with POST method
          fetch('/api/params', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(flightParams)
          }).then(res => console.log(res.ok))
          // .then(() => setFlightStarted(true))
          .then(() => {
            socket.emit('flight-start')
            socket.emit('flight-stats')
        })
          .catch(err => console.log(err))
        } else {
          console.log('Specify all parameters')
        }
        }

      // state of flight start status, changes to true when user submits parameters
      // const [flightStarted, setFlightStarted] = useState(false)

      // state for what page view user is on, starts on mission log screen
      const [page, setPage] = useState('log')

      // Flight Stats state, updates when received form server
      const [flightStats, setFlightStats] = useState({
        'altitude': null,
        'airspeed': null,
        'battery': null,
        'obstacle': null
      })
      // app state for current column drone is on, with an initial state of null
      const [col, setCol] = useState(null)
      // app state for current row drone is on, with an initial state of null
      const [row, setRow] = useState(null)

      // Mission Log
      const [missionLog, setMissionLog] = useState([])
      const missionLogList = missionLog.map((log, index) => 
        <p className='mb-6' key={index}>{log}</p>
      )

      useEffect(() => {
        // on app load, get the time from the server time API
        fetch('/api/time').then(res => res.json()).then(data => {
          setCurrentTime(data.time); 
         });
         // switch on listener for message (for mission log)
         socket.on('message', (data) => {
          const colRegExp = new RegExp('(?<=Column: )[0-9]+')
          const rowRegExp = new RegExp('(?<=Row: )[0-9]+')
          colRegExp.exec(data) && setCol(colRegExp.exec(data)[0])
          rowRegExp.exec(data) && setRow(rowRegExp.exec(data)[0])
          setMissionLog(missionLog => [...missionLog, data])
        })
        // switch on listener for flight status
        socket.on('status', (status) => {
        if (status === 'complete') {
          // setFlightStarted(false)
          // setMissionLog([])
          setCol(0)
          setRow(0)
        }})
         // switch on listener for flight stats
        socket.on('stats', (stats) => {
          try {
            setFlightStats(JSON.parse(stats))
          } catch (error) {
            console.log('Not valid JSON')
            return error;
          }
        })

        return () => {
          socket.disconnect()
        }; // disconnect sockets when app unmounts (is closed)
      }, [])


  return (
    <>
      <PageContext.Provider value={{setPage}}>

        <div className='p-3'>
          {/* Page title */}
          <h1 className='text-4xl text-blue-500'>SeedGenCopter</h1>
          {/* Checks server connection by getting current time from server */}
          <h2 className=' text-base'>Server Status: {currentTime ? currentTime : 'Failed'}</h2>
        </div>

        {/* {!flightStarted && // If the flight has not started render mission parameters page */}
        <>
        <div className='md:grid md:grid-cols-2 items-center max-w-5xl mx-auto'>
          {/* Image showing example mission route */}
          <div className='m-auto container max-w-lg'>
            <img src={Route} alt='Example mission route'/>
          </div>
          {/* Input boxes for flight parameters */}
          <div>
            <h2 className='text-blue-500'>Mission Parameters</h2>
            <form className='my-3 flex flex-col place-items-center text-2xl'>
              <Input name='Height' onChange={e => setDropHeight(e.target.value)} value={dropHeight} unit='m'/>
              <Input name='Spacing' onChange={e => setDropSpacing(e.target.value)} value={dropSpacing} unit='m'/>
              <Input name='Columns' onChange={e => setDropColumns(e.target.value)} value={dropColumns} />
              <Input name='Rows' onChange={e => setDropRows(e.target.value)} value={dropRows}/>
              
            </form>
          </div>

        </div>

        <div className='mt-6'>
            <button 
              className='text-xl md:text-2xl py-2 px-4 mb-8 border-2 rounded-lg border-green-600 hover:bg-green-600 hover:text-white' 
              onClick={() => submitParams()}
              >
                Start Flight
            </button>
          </div>

        <hr className=" border-t-8 my-8 mx-6 rounded-full"></hr>

          {page === 'log' && <MissionLog missionLogList={missionLogList}/>}
          {page === 'stats' && <MissionStats flightStats={flightStats} col={col} row={row}/>}
          {page === 'functions' && <MissionFunctions socket={socket}/>}
          
          <div className='flex flex-row text-center justify-center mt-10 mb-20'>
            <button 
            onClick={() => setPage('log')}
            className={'focus:outline-none' + ((page === 'log') ? ' text-blue-500' : ' text-black')}>
              <BsFillChatSquareDotsFill 
              className='text-5xl mx-10'/>
            </button>
            <button 
            onClick={() => setPage('stats')} 
            className={'focus:outline-none' + ((page === 'stats') ? ' text-blue-500' : ' text-black')}>
              <BsBarChartFill 
              className='text-5xl mx-10'/>
            </button>
            <button onClick={() => setPage('functions')} className={'focus:outline-none' + ((page === 'functions') ? ' text-blue-500' : ' text-black')}>
              <AiFillControl 
              className='text-5xl mx-10'/>
            </button>
            {/* <button onClick={() => setPage('camera')} className={'focus:outline-none' + ((page === 'stats') ? ' text-blue-500' : ' text-black')}>
              <BsBarChartFill className='text-5xl mx-10'/>
            </button> */}
          </div>

          </>
          </PageContext.Provider>
    </>
  );
}

export default App;
