import UploadChatFile from "./UploadChatFile";
import UploadChatText from "./UploadChatText";
import { useState } from "react"
import Button from "./Button";
import SummarizerOptions from "./SummarizerOptions";
import data from "../common/config.json"

const inputOptions = {
    def: 0,
    file: 1,
    transcript: 2
}

const defaultSummarizerOptions = [
    {
        tag: 'useStrict',
        desc: 'Strict Sumamrization',
        selected: false
    },
    {
        tag: 'treatAsMonologue',
        desc: 'Treat transcript as monologue',
        selected: false
    }
]

const SubmitChat = () => {

    const [ selectedInput, setSelectedInput ] = useState(inputOptions.def)
    const [ transcriptText, setTranscriptText ] = useState('')
    const [ summaryOptions, setSummaryOptions ] = useState(defaultSummarizerOptions)

    const toggleOption = (tag) => {
        // use map to set the selected tag to the opposite of whatever it is currently on change
        setSummaryOptions( summaryOptions.map( (opt) => (
            ( opt.tag === tag ) ? { ...opt, selected: !opt.selected } : opt
        )))
    }

    return (
        <div className="basic-container">
            <h1>{data.test}</h1>
            <Button buttonText="Transcript" onClick={() => setSelectedInput(inputOptions.transcript)}/>
            <Button buttonText="Upload File" onClick={() => setSelectedInput(inputOptions.file)}/>
            { (selectedInput === inputOptions.file) && <UploadChatFile />}
            { (selectedInput === inputOptions.transcript) && <UploadChatText transcriptText={transcriptText} setTranscriptText={setTranscriptText}/>}
            { (selectedInput === inputOptions.def) && <br />}
            <SummarizerOptions options={summaryOptions} toggleOption={toggleOption}/>
            <Button buttonText="Summarize!" onClick={() => alert('Submitted!')}/>

        </div>
    )
}

export default SubmitChat