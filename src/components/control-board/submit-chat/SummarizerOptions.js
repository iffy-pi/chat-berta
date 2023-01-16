const SummarizerOptions = ({ options, toggleOption }) => {
    return (
        <div className="basic-container">
            {
            // map is a JS list function , takes a callback
            // and returns a new list where each element was run through the callbackl
            // callback is arrow function shorthand !
            // so returns task headers
            // JSX knows to expand scripts outwards
            options.map( (opt, index) => (
                // Generating list of task components using our Task React component instead
                <div>
                    <input type="checkbox" id={`summarizer_opt_id_${index}`} name={`summarizer_opt_${opt.tag}`} value={opt.tag} checked={opt.selected} onChange={() => toggleOption(opt.tag)}/>
                    <label htmlFor={`summarizer_opt_id_${index}`}>{opt.desc}</label><br/>
                </div>
            ))
        }
        </div>
    )
}

export default SummarizerOptions