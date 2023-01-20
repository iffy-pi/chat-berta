import { useEffect, useState } from 'react'
import { readFileToText, apiJSONFetch } from '../../functions/basefunctions'

const ContentStates = {
    unset: 0,
    loading: 1,
    set: 2
}

const Status = {
    undef: 0,
    success: 1,
    failure: 2
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

        const req = {
            summary_options: request.options,
            chat_text: request.content
        }

        try {
            const [ status, res ] = await apiJSONFetch('submit-chat', 'POST', {}, req)
        
            if ( status !== 200 ) throw new Error('Invalid response: '+res)

            // Success so store the data into the local Summary Request
            setlocalSummaryRequest( {
                status: Status.success,
                options: res.summary_options,
                type: res.status,
                content: res.chat_text
            })
        } catch ( error ){
            console.error(error)
            setlocalSummaryRequest({ status: Status.failure})
        }

        setContentState(ContentStates.set)
    }

    useEffect(  () => {
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

            {/* Errorneous request */}
            { (contentState === ContentStates.set && localSummaryRequest.status !== Status.success) && 
            <div className='basic-container'>
                <p>Request failed!</p>
            </div>
            }

            {/* For loading the actual data */}
            { (contentState === ContentStates.set && localSummaryRequest.status === Status.success) && 
            <div className='basic-container'>
                <p>Options: {localSummaryRequest.options}</p>
                <p>Type: {localSummaryRequest.type}</p>
                <p>Content: {localSummaryRequest.content}</p>
            </div>
            }
        </div>
    )
}

export default SummaryView