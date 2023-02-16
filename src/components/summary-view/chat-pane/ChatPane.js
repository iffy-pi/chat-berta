import Message from "./Message"

const ChatPane = ({ chatPackage }) => {
    
    const messages = chatPackage.messages

    const summaryMessageIDs = chatPackage.summary_messages.map( (message) => message.id)

    return (
        <div className="bcontainer">
            <h3>Chat Pane</h3>
            <p>Messsages collation below should be scrollable</p>
            {
                messages.map( (message) => {
                    return <Message text={message.text} thick={ summaryMessageIDs.includes(message.id) } />
                })
            }
        </div>
    )
}

export default ChatPane