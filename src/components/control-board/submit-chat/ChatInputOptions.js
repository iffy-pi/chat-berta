import { useState } from "react"

const ChatInputOptions = ({ options, returnSelected}) => {
    // initializing the component state to default options to the state
    const [ localOptions, setLocalOptions ] = useState(options)

    const selectOption = (id) => {
        // radio buttons so all other options remain unselected!
        const newopts = localOptions.map( (opt) => (
            ( opt.id === id ) ? { ...opt, selected: true } : { ...opt, selected: false}
        ))
        
        returnSelected( id )

        setLocalOptions( newopts )
    }

    return (
        <div className="basic-container">
            {
            // map is a JS list function , takes a callback
            // and returns a new list where each element was run through the callbackl
            // callback is arrow function shorthand !
            // so returns task headers
            // JSX knows to expand scripts outwards
            localOptions.map( (opt) => (
                <div key={opt.id}>
                    <input type="radio" id={`chat_input_opt_id${opt.id}`} name={`chat_input_${opt.label}`} checked={opt.selected} value={opt.label}  onChange={() => selectOption(opt.id)}/>
                    <label htmlFor={`chat_input_opt_id${opt.id}`}>{opt.label}</label><br/>
                </div>
            ))
        }
        </div>
    )
}

export default ChatInputOptions