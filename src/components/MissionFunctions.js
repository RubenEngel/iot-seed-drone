import React from 'react'
import Button from './Button'

function MissionFunctions() {

    return (
        <>
        <h2>Flight Functions</h2>
        <div className='mission-log md:text-2xl flex flex-col justify-center'>
            <Button
                emit={'drop-seeds'}>
                Drop Seeds
            </Button>
            <Button
                emit={'flight-land'}>
                Land
            </Button>
            <Button
                emit={'flight-home'}>
                Return Home
            </Button>
            <Button 
                colour={'bg-red-700 text-white'} 
                emit={'flight-stop'}>
                Cancel Mission
            </Button>
        </div>
        </>
    )
}

export default MissionFunctions
