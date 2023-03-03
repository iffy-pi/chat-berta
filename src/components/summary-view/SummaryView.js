import { useEffect, useState } from 'react'
import { apiJSONFetch, ContentStates } from '../../functions/basefunctions'
import ChatPane from './chat-pane/ChatPane'
import SummaryContentUnset from './summary-states/SummaryContentUnset'
import SummaryContentLoading from './summary-states/SummaryContentLoading'
import SummaryContentError from './summary-states/SummaryContentError'
import SummaryParagraph from './SummaryParagraph'
import configdata from '../../shared/config.json'

const SummaryView = ({ summaryRequest, summaryResponse }) => {

    const [ contentState, setContentState ] = useState(ContentStates.unset)
    const [ summarySuccess, setSummarySuccess ] = useState(false)
    const [ summaryChatPackage, setSummaryChatPackage ] = useState(null)
    const [ requestError, setRequestError ] = useState('')

    const [ intSummaryResponse, setIntSummaryResponse ] = useState({
        contentState: ContentStates.unset,
        success: false, // Whether the response worked
        body: null, // actual server response
        error: '' // Used if there are any errors
    })

    const characterLimit = useState(configdata.PARAGRAPH_CHAR_LIMIT)

    const handleSummaryRequest = async (request) => {
        const req = {
            summary_options: request.summary_options,
            chat_package: request.chat_package
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

            setSummaryChatPackage(res.content.chat_package)
            setSummarySuccess(true)
        } catch ( error ){
            setRequestError(String(error))
            setSummarySuccess(false)
        }

        setContentState(ContentStates.set)
    }

    // useEffect(  () => {
    //     // on change we handle the summary request by making the api call
    //     if ( summaryRequest !== null ) {
    //         setContentState(ContentStates.loading)
    //         handleSummaryRequest({ ...summaryRequest})
    //     }
    // }, [ summaryRequest ])

    useEffect( () => {
        if ( summaryResponse !== null ){

            console.log('Summary response change!', summaryResponse)
            console.log('====')
            // if ( summaryResponse.state === ContentStates.set ){
            //     // If it is set then we can read content
            //     if ( summaryResponse.success ) {
            //         setSummaryChatPackage(summaryResponse.body.chat_package)
            //     } else { 
            //         setRequestError(summaryResponse.error)
            //     }
    
            //     setSummarySuccess( summaryResponse.success )
            // }
            // setContentState(summaryResponse.state)

            setIntSummaryResponse( summaryResponse )
        }
    }, [ summaryResponse ] )

    const renderContentForState = (contentState) => {
        console.log(intSummaryResponse)
        switch(contentState) {
            case ContentStates.unset:
                return (<SummaryContentUnset />)
            case ContentStates.loading:
                return (<SummaryContentLoading />)
            default:
                return (<div><p>Unknown</p></div>)
        }
    }

    return (
        <div className="summary-view-parent">
            <div className="summary-view">
                <div className='sum-view-header'>
                    <h1>Summary View</h1>
                </div>

                {/* For loading content or no content available */}
                {  ( intSummaryResponse.contentState !== ContentStates.set) && renderContentForState(intSummaryResponse.contentState) }
                
                {/* Errorneous request */}
                { (intSummaryResponse.contentState === ContentStates.set && !intSummaryResponse.success) && <SummaryContentError message={intSummaryResponse.error} />}

                {/* For rendedering returned data */}
                { (intSummaryResponse.contentState === ContentStates.set && intSummaryResponse.success ) && 
                    <div>
                        <SummaryParagraph chatPackage={intSummaryResponse.body.chat_package} characterLimit={characterLimit}/>
                        <ChatPane chatPackage={intSummaryResponse.body.chat_package}/>
                    </div>
                }
            </div>
        </div>
    )
}


export default SummaryView