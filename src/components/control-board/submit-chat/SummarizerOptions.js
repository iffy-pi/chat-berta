import { useState } from 'react'
import DropDownSelector from '../../common/DropDownSelector'

const SummarizerOptions = ({ options, returnOptions, transcriptText }) => {
    
    // initializing the component state to default options to the state
    const [ _options, _setOptions ] = useState(options)

    const _toggleOption = (id) => {
        // use map to set the selected tag to the opposite of whatever it is currently on change
        // flattening out and replacing basic_options field with toggle
        const newopts = { ..._options,  basic_options: _options.basic_options.map( (opt) => (
            ( opt.id === id ) ? { ...opt, selected: !opt.selected } : opt
        )) }
        
        returnOptions(newopts)

        _setOptions( newopts )
    }

    // useEffect(  () => {
    //     // on change we handle the summary request by making the api call
    //     if ( summaryRequest !== null ) {
    //         setContentState(ContentStates.loading)
    //         handleSummaryRequest({ ...summaryRequest})
    //     }
    // }, [ summaryRequest ])

    // Used to fill in the summarize_only_for field in the API request
    const onDropDownSelect = (selectedIndx) => {
        // 0 will be for none/both, so party id will be -1
        // No need to check against 0, -1 is recognized as option not set
        const newopts = { ...options, summarize_only_for: selectedIndx-1}

        returnOptions(newopts)
        _setOptions( newopts )
    }

    return (
        <div className="summarizer-options">
            <div className="sum-opts">
                    <subtitle>Summarizer</subtitle>
                    <subtitle>Options</subtitle>
            </div>
            <div className="sum-opts-checks">
                {
                    // map is a JS list function , takes a callback
                    // and returns a new list where each element was run through the callbackl
                    // callback is arrow function shorthand !
                    // so returns task headers
                    // JSX knows to expand scripts outwards
                    _options.basic_options.map( (opt) => (
                        <div key={opt.id}>
                            <input type="checkbox" id={`summarizer_opt_id_${opt.id}`} name={`summarizer_opt_${opt.tag}`} value={opt.tag} checked={opt.selected} onChange={() => _toggleOption(opt.id)}/>
                            <label htmlFor={`summarizer_opt_id_${opt.id}`}>{opt.desc}</label><br/>
                        </div>
                    ))
                }
                <label>Summarize only for </label>
                <DropDownSelector options={['Both', 'Jane', 'John']} onSelect={onDropDownSelect} />
            </div>
        </div>
    )
}

export default SummarizerOptions