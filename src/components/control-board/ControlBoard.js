import SubmitChat from "./submit-chat/SubmitChat"

const ControlBoard = ({ summaryRequest, setSummaryRequest }) => {
    return (
        <div className="basic-container">
           <h1>Chat-Berta!</h1>
           <h2>The web chat summarization tool!</h2>
           <SubmitChat summaryRequest={summaryRequest} setSummaryRequest={setSummaryRequest}/>
        </div>
    )
}

export default ControlBoard