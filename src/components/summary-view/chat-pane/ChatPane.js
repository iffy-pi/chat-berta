import Message from "./Message"

const ChatPane = ({ chatPackage }) => {
    
    const messages = chatPackage.messages

    const summaryMessageIDs = chatPackage.summary_messages.map( (message) => message.id)

    return (
        <div className="">
            <div className="chatpane-header">
                <h2>Chat Pane</h2>
            </div>
            <div className="chatpane-texts">
                <div className="chatpane-text-info">
                    <p>Summary messages are highlighted in <o>orange!</o></p>
                </div>
                {
                    messages.map( (message) => {
                        return <Message text={message.text} thick={ summaryMessageIDs.includes(message.id) } />
                    })
                }
            </div>
        </div>
    )
}

export default ChatPane