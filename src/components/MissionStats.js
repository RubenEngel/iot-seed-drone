export default function MissionStats({flightStats, row, col}) {
    
    return(
    <>
        <h3>Flight Stats</h3>
        <div className='grid grid-cols-2 grid-rows-6 mission-log'>

            <div>Altitude</div>
            <div>{flightStats.altitude.toFixed(2)}</div>

            <div>Velocity</div>
            <div>{flightStats.airspeed.toFixed(2)}</div>

            <div>Column</div>
            <div>{col ?? 'N/A'}</div>

            <div>Row</div>
            <div>{row ?? 'N/A'}</div>

            <div>Battery</div>
            <div>{flightStats.battery} %</div>

            <div>Obstacles</div>
            <div>{flightStats.obstacle ?? 'None'}</div>

        </div>
    </>)
}