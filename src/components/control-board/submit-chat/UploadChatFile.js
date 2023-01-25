import FileUploader from "../../common/FileUploader"

const UploadChatFile = ({ goodFileUpload, failedFileUpload}) => {
    return (
        <div className="basic-container">
            <label htmlFor="chatfile">Upload chat log file: </label>
            <FileUploader onFileSelectSuccess={goodFileUpload} onFileSelectError={failedFileUpload}/>
        </div>
    )
}

export default UploadChatFile
/*
<form action="/chatSubmitted" method="POST" id="chat_source_form" enctype="multipart/form-data">
            <input type="checkbox" id="0" name="UseStrict" value="UseStrict" />
            <label for="0">UseStrict</label><br />
            <input type="submit" value="Summarize!" />
        </form>
*/