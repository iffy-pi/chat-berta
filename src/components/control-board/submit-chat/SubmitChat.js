import UploadChatFile from "./UploadChatFile";
import UploadChatText from "./UploadChatText";
import { useState, useRef } from "react"
import Button from "../../common/Button";
import SummarizerOptions from "./SummarizerOptions";
import data from "../../../shared/config.json"
import { goodChatFileUpload, chatTextToChatJSON, readFileToText, ContentStates, apiJSONFetch, InputOptions } from "../../../functions/basefunctions";
import ExpectedTranscriptFormat from "./ExpectedTranscriptFormat";


const defaultSummarizerOptions = {
    basic_options: data.SUMMARIZER_OPTIONS.map( (opt, index) => (
        { ...opt, id:index, selected:false}
    )),
    summarize_only_for: -1
}


const SubmitChat = ({ setSummaryResponse, summaryResponse }) => {

    const [ selectedInput, setSelectedInput ] = useState(InputOptions.def)

    // Switching transcript text to state
    const [ transcriptText, setTranscriptText ] = useState('')
    const [ selectedFile, setSelectedFile ] = useState(null)
    const [ fileUploaded, setFileUploaded ] = useState(false)
    const summaryOptions = useRef(defaultSummarizerOptions)

    const saveTranscriptText = (textboxText) => {
       setTranscriptText(textboxText)

    }

    const updateSelectedOptions = ( options ) => {
        summaryOptions.current = options
        // console.log(summaryOptions)
    }

    const failedFileUpload = ( error ) => {
        alert('File upload failed!\nError: '+error)
    }

    const goodFileUpload = ( file ) => {
        setSelectedFile(file)
        setFileUploaded(true)
    }


    const makeSummaryRequest = async (request) => {

        const req = {
            summary_options: request.summary_options,
            chat_package: request.chat_package
        }

        const resp = {
            success: false,
            error: '',
            body:  null,
        }

        // Tell summary view that the content is loading now while we make the request        
        setSummaryResponse({ ...summaryResponse ,  contentState: ContentStates.loading})
        try {
            const res = await apiJSONFetch('submit-chat', 'POST', {}, req)
            
            if ( !res.success ) throw new Error('Invalid response: '+res)

            // On success, return the server response to the system
            resp.success = true
            resp.body = res.content
        } catch ( error ){
            // On error, then we can set the response fields
            resp.success = false
            resp.error = String(error)
        }

        setSummaryResponse({ ...summaryResponse ,  
                contentState: ContentStates.set,
                success: resp.success,
                body: resp.body,
                error: resp.error
            })
    }

    const onSubmit = async () => {
        const request = {
        }

        try {
            if ( selectedInput === InputOptions.file ) {
                
                if ( !fileUploaded ) throw new Error('No file or invalid file uploaded!')
                if ( !goodChatFileUpload(selectedFile) ) throw new Error('Invalid file type. Only text based files are allowed.')

                request.type = 'file'

                try{ 
                    request.chat_package = chatTextToChatJSON( await readFileToText(selectedFile) )
                } catch ( error ) {
                    throw new Error('File Parsing Error: '+String(error.message))
                }
            }

            else if ( selectedInput === InputOptions.text ) {
                if ( transcriptText === "" ) throw new Error('No transcript text!')
                request.type = 'text'

                try{ 
                    request.chat_package = chatTextToChatJSON( transcriptText )
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
        // Make the summary request call
        await makeSummaryRequest(request)
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
            { (selectedInput === InputOptions.text) && <UploadChatText returnText={saveTranscriptText} transcriptText={transcriptText}/>}
            {/* { (selectedInput !== InputOptions.def) && <br />}  */}
            <ExpectedTranscriptFormat />
            <SummarizerOptions options={summaryOptions.current} returnOptions={updateSelectedOptions} selectedInput={selectedInput} transcriptText={transcriptText} uploadedFile={selectedFile}/>
            <div className="center-div">
                <Button className="summarize-btn" buttonText="Summarize!" onClick={onSubmit}/>
            </div>
        </div>
    )
}

export default SubmitChat