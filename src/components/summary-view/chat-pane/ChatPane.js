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
            </div>
            <div className="chatpane-texts">
                <div className="chatpane-text-info">
                    <p>Summary messages are highlighted in <o>orange!</o></p>
                    {/* Do who is sending information here */}
                </div>
                {
                    messages.map( (message) => {
                        return <Message text={message.text} isUsersMessage={message.pid === primaryPartyID} special={ summaryMessageIDs.includes(message.id) } />
                    })
                }
            </div>
        </div>
    )
}

export default ChatPane