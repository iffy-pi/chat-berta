import UploadChatFile from "./UploadChatFile";
import UploadChatText from "./UploadChatText";
import FileUploader from '../../common/FileUploader'
import { useState, useRef } from "react"
import Button from "../../common/Button";
import SummarizerOptions from "./SummarizerOptions";
import data from "../../../shared/config.json"

const inputOptions = {
    def: 0,
    file: 1,
    transcript: 2
}

const defaultSummarizerOptions = [
    {
        id: 0,
        tag: 'useStrict',
        desc: 'Strict Sumamrization',
        selected: false
    },
    {
        id: 1,
        tag: 'treatAsMonologue',
        desc: 'Treat transcript as monologue',
        selected: false
    }
]

const SubmitChat = () => {

    const [ selectedInput, setSelectedInput ] = useState(inputOptions.def)

    const transcriptText = useRef('')
    const summaryOptions = useRef(defaultSummarizerOptions)

    const saveTranscriptText = (textboxText) => {
       transcriptText.current = textboxText 
    }

    const updateSelectedOptions = ( options ) => {
        summaryOptions.current = options
    }

    return (
        <div className="basic-container">
            <h1>{data.test}</h1>
            <Button buttonText="Transcript" onClick={() => setSelectedInput(inputOptions.transcript)}/>
            <Button buttonText="Upload File" onClick={() => setSelectedInput(inputOptions.file)}/>
            { (selectedInput === inputOptions.file) && <UploadChatFile />}
            { (selectedInput === inputOptions.transcript) && <UploadChatText returnText={saveTranscriptText}/>}
            { (selectedInput === inputOptions.def) && <br />}
            <SummarizerOptions options={summaryOptions.current} returnOptions={updateSelectedOptions}/>
            <Button buttonText="Summarize!" onClick={() => alert('Submitted!: '+ summaryOptions.current[0] +' '+summaryOptions.current[0].selected)}/>
            {/* <FileUploader /> */}

        </div>
    )
}

export default SubmitChat