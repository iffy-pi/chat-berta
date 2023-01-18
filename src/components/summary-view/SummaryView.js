import { useEffect, useState } from 'react'
import { readFileToText } from '../../functions/basefunctions'

const ContentStates = {
    unset: 0,
    loading: 1,
    set: 2
}

const SummaryView = ({ summaryRequest, setSummaryRequest }) => {

    const [ localSummaryRequest, setlocalSummaryRequest ] = useState(null)
    const [ contentState, setContentState ] = useState(ContentStates.unset)

    const unpackSummaryRequest = async (request) => {
        // unpack the file if the request package is a file
        console.log('Unpacking request')

        console.log(request)

        if ( request.type === 'file' ) {
            request.content = await readFileToText(request.file)
        }

        // API call can be placed here!!!

        setContentState(ContentStates.set)
        setlocalSummaryRequest(request)
    }

    useEffect( () => {
        // on change of summaryRequest, we want to populate our local summary request
        // with the information
        if ( summaryRequest !== null ) {
            setContentState(ContentStates.loading)
            unpackSummaryRequest({ ...summaryRequest})
        }
    }, [ summaryRequest ])

    const renderContentState = (contentState) => {
        switch(contentState) {
            case ContentStates.unset:
                return 'No content available'
            case ContentStates.loading:
                return 'Content Loading'
            default:
                return 'UNKNOWN!'
        }
    }

    return (
        <div className="basic-container">
            <h1>Summary View</h1>
            <p>This will contain the information about the rendered summary</p>
            {  ( contentState !== ContentStates.set) && <p>{renderContentState(contentState)}</p>}

            { (localSummaryRequest !== null ) && 
            <div>
                <p>Options: {localSummaryRequest.options}</p>
                <p>Type: {localSummaryRequest.type}</p>
                <p>Content: {localSummaryRequest.content}</p>
            </div>
            }
        </div>
    )
}

export default SummaryView