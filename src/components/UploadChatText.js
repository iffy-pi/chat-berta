const UploadChatText = ({ transcriptText, setTranscriptText }) => {
    return (
        <div className="basic-container">
            <p><label htmlFor="transcript_text_box">Paste Dialog Transcript Below:</label></p>
            <textarea id="transcript_text_box" name="transcript_text" rows="10" cols="75" placeholder="Type/Paste here!" value={transcriptText} onChange={(e) => setTranscriptText(e.target.value)}></textarea>
        </div>
    )
}

export default UploadChatText