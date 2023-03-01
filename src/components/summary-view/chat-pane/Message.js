import { useState, useEffect } from 'react' 

const Message = ({ text, color, isSelfMessage, special }) => {
    const [ messageStyle, setMessageStyle ] = useState('chatpane-message')

    useEffect( () => {
        let style = "chatpane-message"
        if ( isSelfMessage ) style += " self-message"
        if ( special )  style += " special-message"

        setMessageStyle( style );
    }, [])

    return (
        // Anchor the message to the right with users-message css if it is from user
        // Otherwise anchored to the left
        <div className={(isSelfMessage) ? "right-align-div" : ""}>
            <div className={messageStyle}>
                <p>{text}</p>
            </div>
        </div>
    )
}

Message.defaultProps = {
    special: false, // if it is a summary message
    isSelfMessage: true // if the message is from the current user, used in determining alignment 
}

export default Message