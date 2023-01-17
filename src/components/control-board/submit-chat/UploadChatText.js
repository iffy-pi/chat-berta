import { useState } from "react"

const UploadChatText = ({ returnText }) => {
    const [ _transcriptText, _setTranscriptText ] = useState('')

    const onTextChange = (newText) => {
        // we set the transcript text and return to parent component
        returnText(newText)
        // Also update our current state
        _setTranscriptText(newText)
    }

    return (
        <div className="basic-container">
            <p><label htmlFor="transcript_text_box">Paste Dialog Transcript Below:</label></p>
            <textarea 
            id="transcript_text_box" 
            name="transcript_text" 
            rows="10" cols="75" 
            placeholder="Type/Paste transcript here!" 
            value={_transcriptText} 
            onChange={(e) => onTextChange(e.target.value)} />
        </div>
    )
}

export default UploadChatText