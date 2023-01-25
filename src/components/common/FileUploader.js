import { goodChatFileUpload } from '../../functions/basefunctions'

const FileUploader = ({onFileSelectSuccess, onFileSelectError}) => {
    const handleFileInput = (e) => {
        // handle validations
        try {
            // check if we actually do have any files
            if ( e.target.files.length === 0) {
                throw new Error('No file selected!')
            }

            // check the file extensions, only expecting text
            const file = e.target.files[0]
            
            if ( !goodChatFileUpload(file) ) throw new Error('Invalid file type. Only text based files are allowed.')

            // all good
            onFileSelectSuccess(file)
        } catch ( error ){
            // if error occured, return onFileFailure
            onFileSelectError(String(error))
        }
    }

    return (
        <div className="file-uploader">
            <input type="file" onChange={handleFileInput} />
            {/* <button onClick={e => fileInput.current && fileInput.current.click()} >Me!</button> */}
        </div>
    )
}

export default FileUploader