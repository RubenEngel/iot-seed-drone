const Input = ({name, onChange, value}) => {

return(
<div className="container max-w-screen-sm grid grid-cols-2 gap-0 overflow-hidden my-3 px-6">
    <div>
        <label>{name}</label>
    </div>
    <div>
        <input className='border-2 rounded-lg max-w-lg w-20' onChange={onChange} value={value} type="number"/>
        <p className='inline ml-2'>m</p>
    </div>
</div>
)
}
export default Input