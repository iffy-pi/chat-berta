import { useEffect, useState } from 'react'
import { readFileToText, apiJSONFetch } from '../../functions/basefunctions'
import logo from '../../media/react-logo.svg'
import ChatPane from './chat-pane/ChatPane'

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
    const [ summarySuccess, setSummarySuccess ] = useState(false)
    const [ summaryResponseChat, setSummaryResponseChat ] = useState(null)

    const unpackSummaryRequest = async (request) => {
        // unpack the file if the request package is a file
        console.log('Unpacking request')

        const req = {
            summary_options: request.options,
            parsed_chat: request.content
        }

        try {
            const res = await apiJSONFetch('submit-chat', 'POST', {}, req)
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            // console.log(res)


            // Success so store the data into the local Summary Request
            // setlocalSummaryRequest( {
            //     status: Status.success,
            //     options: res.content.summary_options,
            //     type: res.content.status,
            //     content: JSON.stringify(res.content.parsed_chat)
            // })

            setSummaryResponseChat(res.content.parsed_chat)
            setSummarySuccess(true)
        } catch ( error ){
            console.error(error)
            setSummarySuccess(false)
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
                return (<div><p>No content available</p></div>)
            case ContentStates.loading:
                return (
                    <div>
                        <p>Loading...</p>
                    </div>
                )
            default:
                return (<div><p>Unknown</p></div>)
        }
    }

    return (
        <div className="basic-container">
            <h1>Summary View</h1>
            <p>This will contain the information about the rendered summary</p>
            {  ( contentState !== ContentStates.set) && renderContentState(contentState) }

            {/* Errorneous request */}
            { (contentState === ContentStates.set && !summarySuccess) && 
            <div className='basic-container'>
                <p>Request failed!</p>
            </div>
            }

            {/* For loading the actual data */}
            { (contentState === ContentStates.set && summarySuccess ) && 
            <div className='basic-container'>
                <ChatPane chatPackage={summaryResponseChat}/>
            </div>
            }
        </div>
    )
}

export default SummaryView