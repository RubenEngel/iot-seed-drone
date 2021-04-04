import Button from './Button'
import React from 'react'
import ReactPlayer from 'react-player'

function Camera() {
    return (
        <>
        <h2>Camera</h2>
        <div className='mission-log md:text-2xl flex flex-col justify-center'>
            <p className='font-bold mb-2'>Live Stream</p>
            <div className='player-wrapper w-full test mx-auto mb-8'>
                <ReactPlayer 
                url='127.0.0.1:8080/stream' 
                width='100%'
                height='100%'
                />
            </div>
            
            <Button
            
            >
                Capture Image
            </Button>
            <Button
            
            >
                Download Image
            </Button>
        </div>
        </>
    )
}

export default Camera
