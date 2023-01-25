import UploadChatFile from "./UploadChatFile";
import UploadChatText from "./UploadChatText";
import { useState, useRef } from "react"
import Button from "../../common/Button";
import SummarizerOptions from "./SummarizerOptions";
import data from "../../../shared/config.json"
import { goodChatFileUpload, chatTextToChatJSON, readFileToText } from "../../../functions/basefunctions";

const InputOptions = {
    def: 0,
    file: 1,
    text: 2
}

const defaultSummarizerOptions = data.SUMMARIZER_OPTIONS.map( (opt, index) => (
    { ...opt, id:index, selected:false}
))

const SubmitChat = ({ setSummaryRequest }) => {

    const [ selectedInput, setSelectedInput ] = useState(InputOptions.def)

    const transcriptText = useRef('')
    const summaryOptions = useRef(defaultSummarizerOptions)
    const selectedFile = useRef(null)
    const fileUploaded = useRef(false)

    const saveTranscriptText = (textboxText) => {
       transcriptText.current = textboxText 
    }

    const updateSelectedOptions = ( options ) => {
        summaryOptions.current = options
    }

    const failedFileUpload = ( error ) => {
        alert('File upload failed!\nError: '+error)
    }

    const goodFileUpload = ( file ) => {
        selectedFile.current = file
        fileUploaded.current = true
    }

    const onSubmit = async () => {
        const request = {}

        try {
            if ( selectedInput === InputOptions.file ) {
                
                if ( !fileUploaded.current ) throw new Error('No file or invalid file uploaded!')
                if ( !goodChatFileUpload(selectedFile.current) ) throw new Error('Invalid file type. Only text based files are allowed.')

                request.type = 'file'
                request.chat_package = chatTextToChatJSON( await readFileToText(selectedFile.current) )
            }

            else if ( selectedInput === InputOptions.text ) {
                if ( transcriptText.current === "" ) throw new Error('No transcript text!')
                request.type = 'text'
                request.chat_package = chatTextToChatJSON( transcriptText.current )

            } else {
                throw new Error('No chat input selected!')
            }

        } catch(error){
            alert('Submission Failed!\nReason: '+error)
            return
        }

        request.options = summaryOptions.current.filter( opt => opt.selected).map( (opt) => opt.tag)

        //console.log(request)
        setSummaryRequest(request)
    }

    

    return (
        <div className="basic-container">
            <h2>Submit A Chat Request</h2>
            <Button buttonText="Transcript" onClick={() => setSelectedInput(InputOptions.text)}/>
            <Button buttonText="Upload File" onClick={() => setSelectedInput(InputOptions.file)}/>
            { (selectedInput === InputOptions.file) && <UploadChatFile goodFileUpload={goodFileUpload} failedFileUpload={failedFileUpload}/>}
            { (selectedInput === InputOptions.text) && <UploadChatText returnText={saveTranscriptText} transcriptText={transcriptText.current}/>}
            { (selectedInput === InputOptions.def) && <br />}
            <SummarizerOptions options={summaryOptions.current} returnOptions={updateSelectedOptions}/>
            <Button buttonText="Summarize!" onClick={onSubmit}/>
        </div>
    )
}

export default SubmitChat