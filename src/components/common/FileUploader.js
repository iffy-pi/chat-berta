import { useEffect, useState } from 'react'

const dt = new DataTransfer();
const emptyFileList = dt.files

const FileUploader = ({onFileSelectSuccess, onFileSelectError, id, validFile, fileList}) => {

    const [ _fileList, _setFileList ] = useState(fileList)

    useEffect( () => {
        // Update the actual tag in the DOM
        const fileInput = document.querySelector(`#${id}`)
        fileInput.files = _fileList
    }, [_fileList])

    const handleFileInput = (e) => {
        // handle validations
        try {
            // check if we actually do have any files
            if ( e.target.files.length < 1) {
                throw new Error('No file selected')
            }

            // validate file list
            for ( let i=0; i < e.target.files.length; i++){
                if ( !validFile(e.target.files[i]) ) throw new Error('Invalid file type') 
            }

            // set the file list for the state
            _setFileList(e.target.files)

            // all good
            onFileSelectSuccess(e.target.files)
        
        } catch ( error ){
            
            // reset file uploaded
            _setFileList(emptyFileList)

            // if error occured, return onFileFailure
            onFileSelectError(error)
        }
    }

    return (
        <div className="file-uploader">
            <input type="file" id={id} onChange={handleFileInput}/>
        </div>
    )
}

FileUploader.defaultProps = {
    onFileSelectError: (err) => { }, // receives exception thrown
    onFileSelectSuccess: (fileList) => { }, // receives a fileList object that contains the files
    fileList: emptyFileList,
    validFile: (file) => { return true}, // function to run on each file to validate files
    id: "file-uploader"
}

export default FileUploader