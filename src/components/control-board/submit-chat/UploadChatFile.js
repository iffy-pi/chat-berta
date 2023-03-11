import FileUploader from "../../common/FileUploader"
import { goodChatFileUpload } from '../../../functions/basefunctions'

const UploadChatFile = ({ goodFileUpload, failedFileUpload, fileList}) => {

    return (
        <div className="chat-src-panel">
            <smalltitle>Upload chat log file: </smalltitle>
            <FileUploader onFileSelectSuccess={goodFileUpload} onFileSelectError={failedFileUpload} 
            validFile={goodChatFileUpload} fileList={fileList} id="upload-chat-file"/>
        </div>
    )
}

export default UploadChatFile