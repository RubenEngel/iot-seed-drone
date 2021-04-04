import React from 'react'
import Button from './Button'

function MissionFunctions({socket}) {

    return (
        <>
        <h2>Flight Functions</h2>
        <div className='mission-log flex flex-col justify-center'>
            <Button
                emit={'drop-seeds'}
                socket={socket}>
                Drop Seeds
            </Button>
            <Button
                emit={'flight-land'} 
                socket={socket}>
                Land
            </Button>
            <Button
                emit={'flight-home'} 
                socket={socket}>
                Return Home
            </Button>
            <Button 
                colour={'bg-red-700 text-white'} 
                emit={'flight-stop'} 
                socket={socket}>
                Cancel Mission
            </Button>
        </div>
        </>
    )
}

export default MissionFunctions
