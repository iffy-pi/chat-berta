

// returns true if file is a good upload and false if not
const goodChatFileUpload = (file) => {
    if ( file.type === "" || !file.type.startsWith('text/') ) return false
    return true
}

const readFileToText = file => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.addEventListener('load', () => resolve(reader.result))
    reader.addEventListener('error', () => reject('Reading file failed'))
    reader.readAsText(file)
})

export {
    goodChatFileUpload,
    readFileToText
}