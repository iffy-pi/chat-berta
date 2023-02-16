import SubmitChat from "./submit-chat/SubmitChat"

const ControlBoard = ({ summaryRequest, setSummaryRequest }) => {
    return (
        <div className="bcontainer control-board-parent">
            <div className="control-board">
                <div className="control-board-header">
                    <h1>Chat-Berta!</h1>
                    <p className="control-board-subtitle">The web chat summarization tool!</p>
                </div>
                <SubmitChat summaryRequest={summaryRequest} setSummaryRequest={setSummaryRequest}/>
            </div>
        </div>
    )
}

export default ControlBoard