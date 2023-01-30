import { useState } from "react"
import Button from "../../common/Button"

// JS component that just contains the expected format for the transcript
const ExpectedTranscriptFormat = () => {

    const [ chatExample, setChatExample ] = useState("")
    const [ showExample, setShowExample ] = useState(false)

    const toggleShowExample = () => {
        setShowExample(!showExample)
    }

    return (
        <div className='basic-container'>
            <Button buttonText={ (showExample) ? "Hide Transcript Format" : "Show Transcript Format" } onClick={toggleShowExample}/>
            {
                ( showExample ) && 
                <div>
                    <h2>Expected Chat Format</h2>
                    <p>Chats include the party names indicated with a colon, and the messages sent by each party. Party messages are indented (either by spaces or tabs) from the beginning of the line to differentiate them from the party sender lines. An example is included below:</p>
                    <pre><code>John:
            I like apples
            What is your favourite fruit?
        Jane:
            I like oranges better, apples be gross sometimes
        John:
            Oh really, I think apples are superior
        Janet:
            Interesting</code></pre>
                </div>
            }
        </div>
    )
}

export default ExpectedTranscriptFormat