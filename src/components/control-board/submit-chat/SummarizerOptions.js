import { useState, useEffect } from 'react'
import DropDownSelector from '../../common/DropDownSelector'
import {chatTextToChatJSON, readFileToText, goodChatFileUpload, InputOptions } from "../../../functions/basefunctions";

function useDebounceValue( value, time) {
    // value is what we are debouncing
    // time is the wait time in ms

    // first define a state to hold the debounce value
    const [ debounceValue, setDebounceValue ] = useState(value)

    // Then we use useEffect to track the value
    useEffect( () => {

        // Start a timer which will set the debouncevalue after timeout
        const timeout = setTimeout( () => { setDebounceValue(value) }, time)

        // Returning cleanup function for use-effect
        // Clean up clears the previous timeout
        return () => {
            clearTimeout(timeout)
        }
    },
    // dependency is value and time, meaning it is run anytime value or time changes
    // meaning it is re-run anytime the value being set changes so it resets the timer
        // re-running involves clearing previous useEffect which runs cleanup function and clears previously set timeout
        // therefore, when value changes a new timer is set which effectively resets our timeout
    [value, time])

    return debounceValue
}

const SummarizerOptions = ({ options, returnOptions, selectedInput, transcriptText, uploadedFile  }) => {
    
    // initializing the component state to default options to the state
    const [ _options, _setOptions ] = useState(options)
    const [ partyDropDown, setPartyDropDown ] = useState([])
    // Debouncing to allow for user to finish typing
    const debouncedText = useDebounceValue(transcriptText, 300)

    const _toggleOption = (id) => {
        // use map to set the selected tag to the opposite of whatever it is currently on change
        // flattening out and replacing basic_options field with toggle
        const newopts = { ..._options,  basic_options: _options.basic_options.map( (opt) => (
            ( opt.id === id ) ? { ...opt, selected: !opt.selected } : opt
        )) }
        
        returnOptions(newopts)

        _setOptions( newopts )
    }

    const getPartiesList = (chat_package) => {
        return chat_package.config.parties.map( (party) => party.name)
    }

    // Used to fill in the summarize_only_for field in the API request
    const onDropDownSelect = (selectedIndx) => {
        // 0 will be for none/both, so party id will be -1
        // No need to check against 0, -1 is recognized as option not set
        const newopts = { ...options, summarize_only_for: selectedIndx-1}

        returnOptions(newopts)
        _setOptions( newopts )
    }

    const parsePartiesForFile = async (uploadedFile) => {
        try {
            if ( uploadedFile === null ) throw new Error('No file uploaded')
            if ( !goodChatFileUpload(uploadedFile) ) throw new Error('Bad file format')
            const chat_package = chatTextToChatJSON( await readFileToText(uploadedFile) )
            setPartyDropDown(getPartiesList(chat_package))
        } catch ( error ) {
            // parsing failed for some reason, set empty parties
            setPartyDropDown([])
        }
    }

    useEffect( () => {
        // Parse parties every time the transcript changes (debounced), uploaded file changes, or input option changes
        try {
            if ( selectedInput === InputOptions.def) throw new Error('No selection')

            if( selectedInput === InputOptions.text ){
                // on change of debounced transcript text we attempt to parse and get party information
                // Only parsing if we are on transcript option
                const chat_package = chatTextToChatJSON( debouncedText )
                setPartyDropDown( getPartiesList(chat_package) )
            }

            else if ( selectedInput === InputOptions.file ){
                // file handled asynchronously
                parsePartiesForFile(uploadedFile)
            }

        } catch (error) {
            // parsing failed for some reason, set empty parties
            setPartyDropDown([])
        }

    }, [ debouncedText, uploadedFile, selectedInput])



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
                <DropDownSelector 
                options={
                    // if no items in the party drop down then just append N/A (means that no parties have been found)
                    // else prepend all 
                    ( partyDropDown.length > 0 ) ? [ 'All' ].concat(partyDropDown) : ['N/A' ] 
                }
                disabled={ ( partyDropDown.length === 0 )}
                onSelect={onDropDownSelect} />
            </div>
        </div>
    )
}

export default SummarizerOptions