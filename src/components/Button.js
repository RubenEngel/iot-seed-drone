import React from 'react'

function Button({socket, emit, colour, children}) {
    return (
        <div>

            <div className={'mb-10'}>
                <button
                className={'border-2 px-4 py-1 rounded-xl ' + colour}
                onClick={() => {
                socket.emit(emit)
                }} >
                 {children}
                </button>
            </div>

        </div>
    )
}

export default Button
