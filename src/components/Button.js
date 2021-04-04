import React from 'react'
import { useContext } from 'react'
import AppContext from '../page-context'


function Button({ emit, colour, children}) {
    
    const { socket, setPage } = useContext( AppContext )

    return (
        <div>

            <div className={'mb-10'}>
                <button
                className={'border-2 px-4 py-1 rounded-xl ' + colour}
                onClick={() => {
                socket.emit(emit)
                setPage('log')
                }} >
                 {children}
                </button>
            </div>

        </div>
    )
}

export default Button
