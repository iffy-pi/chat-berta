import React, {useRef} from 'react'

const FileUploader = ({onFileSelectSuccess, onFileSelectError}) => {
    const fileInput = useRef(null)

    const handleFileInput = (e) => {
        // handle validations
        // we would check extensions
        onFileSelect(e.target.files[0])
    }

    return (
        <div className="file-uploader">
            <input type="file" onChange={handleFileInput} />
            {/* <button onClick={e => fileInput.current && fileInput.current.click()} className="btn btn-primary" /> */}
        </div>
    )
}

export default FileUploader