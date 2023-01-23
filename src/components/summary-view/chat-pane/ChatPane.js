import Message from "./Message"

const ChatPane = ({ chatPackage }) => {
    
    const messages = chatPackage.messages

    const summaryMessageIDs = chatPackage.summary_messages.map( (message) => message.id)

    return (
        <div>
            {
                messages.map( (message) => {
                    return <Message text={message.text} thick={ summaryMessageIDs.includes(message.id) } />
                })
            }
        </div>
    )
}

export default ChatPane