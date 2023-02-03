import { useState } from "react"
import Button from "../../common/Button"

// JS component that just contains the expected format for the transcript
const ExpectedTranscriptFormat = () => {

    const [ chatExample, setChatExample ] = useState("John:\nApples are my favourite fruit, what are yours?\n\nJane:\nI like oranges better, apples be gross sometime\n\nJohn:\nOh really, I think apples are superior\n\nJane:\nInteresting")
    const [ showExample, setShowExample ] = useState(false)

    const toggleShowExample = () => {
        setShowExample(!showExample)
    }

    

    return (
        <div className='basic-container'>
            <h2>Expected Chat Format</h2>
            {
                ( showExample ) && 
                <div>
                    <p>Chats include the party names indicated with a colon, and the messages sent by each party. Party messages are indented (either by spaces or tabs) from the beginning of the line to differentiate them from the party sender lines. An example is shown below:</p>
                    <code className="code-block">{chatExample}</code>
                </div>
            }
            <Button buttonText={ (showExample) ? "Hide Transcript Format" : "Show Transcript Format" } onClick={toggleShowExample}/>
        </div>
    )
}

export default ExpectedTranscriptFormat