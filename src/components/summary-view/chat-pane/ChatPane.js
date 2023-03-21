import Message from "./Message"
import { useState } from "react"
import DropDownSelector from "../../common/DropDownSelector"

const ChatPane = ({ chatPackage }) => {
    
    const messages = chatPackage.messages

    const summaryMessageIDs =  chatPackage.summary.message_ids //chatPackage.summary_messages.map( (message) => message.id)

    const [ partyOpts, setPartyOpts ] = useState( chatPackage.config.parties.map( (party) => party.name))
    const [ primaryPartyID , setPrimaryPartyID ] = useState(0)

    const onPartySelect = (selectedPartyID) => {
        // Set the primary party to the selected party from the drop down
        setPrimaryPartyID( selectedPartyID )
    }

    return (
        <div className="">
            <div className="chatpane-header">
                <h2>Chat Pane</h2>
                {/* Place primary party here */}
                <label>Messages are rendered from </label>
                <DropDownSelector options={partyOpts} name="primary_party_selector" onSelect={onPartySelect}/>
                <label> 's point of view.</label>
            </div>
            <div className="chatpane-texts-parent">
                <div className="chatpane-texts">
                    <div className="chatpane-text-info">
                        <p>Summary messages are highlighted in <o>orange!</o></p>
                    </div>
                    {
                        messages.map( (message) => {
                            // Message is special if the message id is in the summary message ids
                            return <Message text={message.text} isSelfMessage={message.pid === primaryPartyID} special={ summaryMessageIDs.includes(message.id) } />
                        })
                    }
                </div>
            </div>
        </div>
    )
}

export default ChatPane