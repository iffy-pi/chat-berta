import { useEffect, useState } from 'react'
import { apiJSONFetch, ContentStates } from '../../functions/basefunctions'
import ChatPane from './chat-pane/ChatPane'
import SummaryContentUnset from './summary-states/SummaryContentUnset'
import SummaryContentLoading from './summary-states/SummaryContentLoading'
import SummaryContentError from './summary-states/SummaryContentError'
import SummaryParagraph from './SummaryParagraph'
import configdata from '../../shared/config.json'

const SummaryView = ({ summaryResponse }) => {

    const characterLimit = useState(configdata.PARAGRAPH_CHAR_LIMIT)

    const renderContentForState = (contentState) => {
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
                {  ( summaryResponse.contentState !== ContentStates.set) && renderContentForState(summaryResponse.contentState) }
                
                {/* Errorneous request */}
                { (summaryResponse.contentState === ContentStates.set && !summaryResponse.success) && <SummaryContentError message={summaryResponse.error} />}

                {/* For rendedering returned data */}
                { (summaryResponse.contentState === ContentStates.set && summaryResponse.success ) && 
                    <div>
                        <SummaryParagraph chatPackage={summaryResponse.body.chat_package} characterLimit={characterLimit}/>
                        <ChatPane chatPackage={summaryResponse.body.chat_package}/>
                    </div>
                }
            </div>
        </div>
    )
}


export default SummaryView