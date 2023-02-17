import { useState, useEffect } from 'react' 

const Message = ({ text, color, isUsersMessage, special }) => {
    const [ messageStyle, setMessageStyle ] = useState('chatpane-message')

    useEffect( () => {
        let style = "chatpane-message"
        if ( special )  style += " special"

        setMessageStyle( style );
    }, [])

    return (
        // Anchor the message to the right with users-message css if it is from user
        // Otherwise anchored to the left
        <div className={(isUsersMessage) ? "users-message" : ""}>
            <div className={messageStyle}>
                <p>{text}</p>
            </div>
        </div>
    )
}

Message.defaultProps = {
    special: false, // if it is a summary message
    isUsersMessage: true // if the message is from the current user, used in determining alignment 
}

export default Message