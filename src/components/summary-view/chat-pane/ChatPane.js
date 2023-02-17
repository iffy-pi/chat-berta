import Message from "./Message"

const ChatPane = ({ chatPackage }) => {
    
    const messages = chatPackage.messages

    const summaryMessageIDs = chatPackage.summary_messages.map( (message) => message.id)

    // Using first pid as the primary party but could not be the case
    // Will implement user input for it
    const primaryPartyID = chatPackage.messages[0].pid

    return (
        <div className="">
            <div className="chatpane-header">
                <h2>Chat Pane</h2>
                {/* Place primary party here */}
                <p>Messages are rendered in primary party's point of view.</p>
            </div>
            <div className="chatpane-texts-parent">
                <div className="chatpane-texts">
                    <div className="chatpane-text-info">
                        <p>Summary messages are highlighted in <o>orange!</o></p>
                    </div>
                    {
                        messages.map( (message) => {
                            // Message is special if the message id is in the summary message ids
                            return <Message text={message.text} isUsersMessage={message.pid === primaryPartyID} special={ summaryMessageIDs.includes(message.id) } />
                        })
                    }
                </div>
            </div>
        </div>
    )
}

export default ChatPane