import UploadChatFile from "./UploadChatFile";
import UploadChatText from "./UploadChatText";
import { useState, useRef } from "react"
import Button from "../../common/Button";
import SummarizerOptions from "./SummarizerOptions";
import data from "../../../shared/config.json"
import { goodChatFileUpload, readFileToText, apiJSONFetch } from "../../../functions/basefunctions";

const inputOptions = {
    def: 0,
    file: 1,
    text: 2
}

const defaultSummarizerOptions = data.SUMMARIZER_OPTIONS.map( (opt, index) => (
    { ...opt, id:index, selected:false}
))

const SubmitChat = () => {

    const [ selectedInput, setSelectedInput ] = useState(inputOptions.def)

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

    const submitSummaryRequest = async (summary_options, chat_text) => {
        const req = {
            summary_options: summary_options,
            chat_text: chat_text
        }

        try {
            const [ status, res ] = await apiJSONFetch('submit-chat', 'POST', {}, req)
        
            if ( status !== 200 ) throw new Error('Invalid response: '+res)

            // alert('Success!\n'+String(res))
            console.log('Success;', res)
        } catch ( error ){
            console.error(error)
        }
    }

    const onSubmit = async () => {

        let uploadContent = ""

        try {
            if ( selectedInput === inputOptions.def ) throw new Error('No chat input selected!')

            if ( selectedInput === inputOptions.file ) {
                
                if ( !fileUploaded.current ) throw new Error('No file or invalid file uploaded!')
                if ( !goodChatFileUpload(selectedFile.current) ) throw new Error('Invalid file type. Only text based files are allowed.')

                // read the contents from th e file
                uploadContent = await readFileToText(selectedFile.current)
            }

            else if ( selectedInput === inputOptions.text ) {
                if ( transcriptText.current === "" ) throw new Error('No transcript text!')
                uploadContent = transcriptText.current
            }

        } catch(error){
            alert('Submission Failed!\nReason: '+error)
            return
        }

        console.log('Valid submission')
        console.log(`Type: ${ (selectedInput === inputOptions.file) ? 'file' : 'text'}`)
        console.log(summaryOptions.current)
        console.log(uploadContent)

        submitSummaryRequest(
            summaryOptions.current.map( (opt) => ( opt.tag )),
            uploadContent
        )

    }

    

    return (
        <div className="basic-container">
            <h1>{data.test}</h1>
            <Button buttonText="Transcript" onClick={() => setSelectedInput(inputOptions.text)}/>
            <Button buttonText="Upload File" onClick={() => setSelectedInput(inputOptions.file)}/>
            { (selectedInput === inputOptions.file) && <UploadChatFile goodFileUpload={goodFileUpload} failedFileUpload={failedFileUpload}/>}
            { (selectedInput === inputOptions.text) && <UploadChatText returnText={saveTranscriptText}/>}
            { (selectedInput === inputOptions.def) && <br />}
            <SummarizerOptions options={summaryOptions.current} returnOptions={updateSelectedOptions}/>
            <Button buttonText="Summarize!" onClick={onSubmit}/>
        </div>
    )
}

export default SubmitChat