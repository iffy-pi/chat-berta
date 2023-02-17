import { useEffect, useState } from 'react'
import { apiJSONFetch } from '../../functions/basefunctions'
import ChatPane from './chat-pane/ChatPane'
import SummaryContentUnset from './summary-states/SummaryContentUnset'
import SummaryContentLoading from './summary-states/SummaryContentLoading'
import SummaryContentError from './summary-states/SummaryContentError'
import SummaryParagraph from './SummaryParagraph'
import configdata from '../../shared/config.json'

const ContentStates = {
    unset: 0,
    loading: 1,
    set: 2
}

const SummaryView = ({ summaryRequest }) => {

    const [ contentState, setContentState ] = useState(ContentStates.unset)
    const [ summarySuccess, setSummarySuccess ] = useState(false)
    const [ summaryChatPackage, setSummaryChatPackage ] = useState(null)
    const [ requestError, setRequestError ] = useState('')
    const [ characterLimit, setCharacterLimit ] = useState(configdata.PARAGRAPH_CHAR_LIMIT)

    const handleSummaryRequest = async (request) => {
        const req = {
            summary_options: request.options,
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

    useEffect(  () => {
        // on change we handle the summary request by making the api call
        if ( summaryRequest !== null ) {
            setContentState(ContentStates.loading)
            handleSummaryRequest({ ...summaryRequest})
        }
    }, [ summaryRequest ])

    const renderUnserContentState = (contentState) => {
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
        <div className="bcontainer summary-view-parent">
            <div className="summary-view">
                <div className='sum-view-header'>
                    <h1>Summary View</h1>
                </div>

                {/* For loading content or no content available */}
                {  ( contentState !== ContentStates.set) && renderUnserContentState(contentState) }

                {/* Errorneous request */}
                { (contentState === ContentStates.set && !summarySuccess) && <SummaryContentError message={requestError} />}

                {/* For rendedering returned data */}
                { (contentState === ContentStates.set && summarySuccess ) && 
                <div>
                    <SummaryParagraph chatPackage={summaryChatPackage} characterLimit={characterLimit}/>
                    <ChatPane chatPackage={summaryChatPackage}/>
                </div>
                }
            </div>
        </div>
    )
}

export default SummaryView