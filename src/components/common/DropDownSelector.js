import { useState } from "react"
import Button from "./Button"

const DropDownSelector = ( {options, onSelect, name, id, className} ) => {
    // onSelect takes the selected option  index as a parameter
    // first option is always the first selected
    const [ selectedOptId, setSelectedOptId ] = useState(0)

    return (
        <select className={className} name={name} id={id}
        onChange={(e) => {
            setSelectedOptId(e.target.selectedIndex)
            onSelect(e.target.selectedIndex)
        }}
        >
            {
                options.map( (opt, i) => (
                    ( i == selectedOptId ) ?
                    <option value={opt} selected="selected">{opt}</option> :
                    <option value={opt}>{opt}</option>
                ))
            }
        </select>
)
}

DropDownSelector.defaultProps = {
    name: 'dropdown',
    id: '',
    className: 'dropdown'
}

export default DropDownSelector