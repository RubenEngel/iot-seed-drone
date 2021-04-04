import Button from './Button'
import React from 'react'

function Camera() {
    return (
        <>
        <h2>Camera</h2>
        <div className='mission-log md:text-2xl flex flex-col justify-center'>
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
