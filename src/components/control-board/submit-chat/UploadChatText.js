import { useState } from "react"

const UploadChatText = ({ returnText, transcriptText }) => {
    const [ _transcriptText, _setTranscriptText ] = useState(transcriptText)

    const onTextChange = (newText) => {
        // we set the transcript text and return to parent component
        returnText(newText)
        // Also update our current state
        _setTranscriptText(newText)
    }

    return (
        <div className="chat-src-panel">
            <smalltitle>Paste Dialog Transcript Below:</smalltitle>
            <textarea 
            id="transcript_text_box" 
            name="transcript_text" 
            rows="20" cols="50" 
            placeholder="Type/Paste transcript here!" 
            value={_transcriptText} 
            onChange={(e) => onTextChange(e.target.value)} />
        </div>
    )
}

export default UploadChatText