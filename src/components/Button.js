import React from 'react'
import { useContext } from 'react'
import PageContext from '../page-context'


function Button({socket, emit, colour, children}) {
    
    const { setPage } = useContext( PageContext )

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
