const Input = ({name, onChange, value}) => {

return(
<div className="flex w-md">
    <label>{name}</label>
    <input onChange={onChange} value={value} type="number"/>
</div>
)
}
export default Input