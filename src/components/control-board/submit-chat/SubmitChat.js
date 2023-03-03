import UploadChatFile from "./UploadChatFile";
import UploadChatText from "./UploadChatText";
import { useState, useRef } from "react"
import Button from "../../common/Button";
import SummarizerOptions from "./SummarizerOptions";
import data from "../../../shared/config.json"
import { goodChatFileUpload, chatTextToChatJSON, readFileToText } from "../../../functions/basefunctions";
import ChatInputOptions from "./ChatInputOptions";
import ExpectedTranscriptFormat from "./ExpectedTranscriptFormat";

const InputOptions = {
    def: 0,
    file: 1,
    text: 2
}

const inputOptionsRendered = [
    {
        'label': 'Paste Transcript',
        'id': InputOptions.text,
        selected: false,
    },
    {
        'label': 'Upload File',
        'id': InputOptions.file,
        selected: false,
    }
]

const defaultSummarizerOptions = {
    basic_options: data.SUMMARIZER_OPTIONS.map( (opt, index) => (
        { ...opt, id:index, selected:false}
    )),
    summarize_only_for: -1
}


const SubmitChat = ({ setSummaryRequest }) => {

    const [ selectedInput, setSelectedInput ] = useState(InputOptions.def)

    const transcriptText = useRef('')
    // Switching transcript text to state
    const [ stateTranscriptText, setStateTranscriptText ] = useState('')
    const summaryOptions = useRef(defaultSummarizerOptions)
    const selectedFile = useRef(null)
    const fileUploaded = useRef(false)

    const saveTranscriptText = (textboxText) => {
       setStateTranscriptText(textboxText)

    }

    const updateSelectedOptions = ( options ) => {
        summaryOptions.current = options
        // console.log(summaryOptions)
    }

    const updateSelectedInput = (inputOption) => {
        setSelectedInput(inputOption)
    } 

    const failedFileUpload = ( error ) => {
        alert('File upload failed!\nError: '+error)
    }

    const goodFileUpload = ( file ) => {
        selectedFile.current = file
        fileUploaded.current = true
    }

    const onSubmit = async () => {
        const request = {
        }

        try {
            if ( selectedInput === InputOptions.file ) {
                
                if ( !fileUploaded.current ) throw new Error('No file or invalid file uploaded!')
                if ( !goodChatFileUpload(selectedFile.current) ) throw new Error('Invalid file type. Only text based files are allowed.')

                request.type = 'file'

                try{ 
                    request.chat_package = chatTextToChatJSON( await readFileToText(selectedFile.current) )
                } catch ( error ) {
                    throw new Error('File Parsing Error: '+String(error.message))
                }
            }

            else if ( selectedInput === InputOptions.text ) {
                if ( stateTranscriptText === "" ) throw new Error('No transcript text!')
                request.type = 'text'

                try{ 
                    request.chat_package = chatTextToChatJSON( stateTranscriptText )
                } catch ( error ) {
                    throw new Error('File Parsing Error: '+String(error.message))
                }

            } else {
                throw new Error('No chat input selected!')
            }

        } catch(error){
            alert('Submission Failed!\nError: '+error.message)
            return
        }

        // Populate request summary options
        // basic options field is updated to be a list of only the selected options
        request.summary_options = { ...summaryOptions.current, basic_options: summaryOptions.current.basic_options.filter( opt => opt.selected).map( (opt) => opt.tag) }


        // console.log(request)
        setSummaryRequest(request)
    }

    

    return (
        <div className="submit-chat-component">
            <div className="submit-chat-section">
                <div className="submit-chat-header">
                    <h2>Submit A</h2>
                    <h2>Chat Request</h2>
                </div>
                <div className="chat-input-options">
                    <p>Select a source:</p>
                    <Button className={"opt-btn" + ((selectedInput === InputOptions.text) ? " opt-btn-clicked": "")}  buttonText="Transcript" onClick={() => setSelectedInput(InputOptions.text)}/>
                    <Button className={"opt-btn" + ((selectedInput === InputOptions.file) ? " opt-btn-clicked" : "")} buttonText="Upload File" onClick={() => setSelectedInput(InputOptions.file)}/>
                </div>
            </div>
            { (selectedInput === InputOptions.file) && <UploadChatFile goodFileUpload={goodFileUpload} failedFileUpload={failedFileUpload}/>}
            { (selectedInput === InputOptions.text) && <UploadChatText returnText={saveTranscriptText} transcriptText={stateTranscriptText}/>}
            {/* { (selectedInput !== InputOptions.def) && <br />}  */}
            <ExpectedTranscriptFormat />
            <SummarizerOptions options={summaryOptions.current} returnOptions={updateSelectedOptions} transcriptText={stateTranscriptText}/>
            <div className="center-div">
                <Button className="summarize-btn" buttonText="Summarize!" onClick={onSubmit}/>
            </div>
        </div>
    )
}

export default SubmitChat