export const Header = () => {
    <div className="header">
        <h1>Seed Planting IoT Drone</h1>
        <h3>Server Connected: {currentTime ? currentTime : 'Failed'}</h3>
    </div>
}