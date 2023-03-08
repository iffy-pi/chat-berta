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
        <div>
            {
                ( showExample ) &&
                <div className='transcript-format'>
                    <div>
                        <subtitle>Expected Chat Format</subtitle>
                        <p>Chats include the party names indicated with a colon, and the messages sent by each party. Party messages are indented (either by spaces or tabs) from the beginning of the line to differentiate them from the party sender lines. An example is shown below:</p>
                        <code className="code-block">{chatExample}</code>
                    </div>
                </div>
            }
            <div className="tfp center-div">
                <Button className={(showExample) ? "clicked" : "" } buttonText={ (showExample) ? "Hide" : "See Expected Format" } onClick={toggleShowExample}/>
            </div>
        </div>
    )
}

export default ExpectedTranscriptFormat