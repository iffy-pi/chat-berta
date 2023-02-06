import SubmitChat from "./submit-chat/SubmitChat"

const ControlBoard = ({ summaryRequest, setSummaryRequest }) => {
    return (
        <div className="bcontainer control-board-parent">
            <div className="bcontainer control-board">
                <h1>Chat-Berta!</h1>
                <h2>The web chat summarization tool!</h2>
                <SubmitChat summaryRequest={summaryRequest} setSummaryRequest={setSummaryRequest}/>
            </div>
        </div>
    )
}

export default ControlBoard