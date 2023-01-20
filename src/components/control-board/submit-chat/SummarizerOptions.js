import { useState } from 'react'

const SummarizerOptions = ({ options, returnOptions }) => {
    
    // initializing the component state to default options to the state
    const [ _options, _setOptions ] = useState(options)

    const _toggleOption = (id) => {
        // use map to set the selected tag to the opposite of whatever it is currently on change
        const newopts = _options.map( (opt) => (
            ( opt.id === id ) ? { ...opt, selected: !opt.selected } : opt
        ))
        
        returnOptions(newopts)

        _setOptions( newopts )
    }

    return (
        <div className="basic-container">
            {
            // map is a JS list function , takes a callback
            // and returns a new list where each element was run through the callbackl
            // callback is arrow function shorthand !
            // so returns task headers
            // JSX knows to expand scripts outwards
            _options.map( (opt) => (
                <div>
                    <input type="checkbox" id={`summarizer_opt_id_${opt.id}`} name={`summarizer_opt_${opt.tag}`} value={opt.tag} checked={opt.selected} onChange={() => _toggleOption(opt.id)}/>
                    <label htmlFor={`summarizer_opt_id_${opt.id}`}>{opt.desc}</label><br/>
                </div>
            ))
        }
        </div>
    )
}

export default SummarizerOptions