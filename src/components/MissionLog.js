import ScrollToBottom from 'react-scroll-to-bottom'

export default function MissionLog({missionLogList}) {
    return(
        <div>
            <h3>Mission Log</h3>
            <ScrollToBottom debug={false} className='mission-log'>
                <ul>{missionLogList}</ul>
            </ScrollToBottom>
        </div>
    )
}