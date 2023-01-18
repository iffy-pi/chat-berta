import { CHAT_BERTA_API } from "../configs/apiconfig";


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

// The api always returns in JSON format, even for errors
// Receives body object that is converted to JSON
async function apiJSONFetch(apiPath, method, headers, body ) {

    const request = {
        method: method
    }

    if ( headers !== null && headers !== {} ){
        request.headers = headers
    }

    if ( body !== null ){
        if ( request.headers['content-type'] === undefined ){
            request.headers['content-type'] = 'application/json'
            request.body = JSON.stringify(body)
        }
    }
    // Make the request
    const res = await fetch(
        `${CHAT_BERTA_API}/${apiPath}`,
        request
    )

    if ( res.status !== 200 ){
        // check if it is a client side error, api always returns 400,
        // if it is then we can return the JSON message
        if ( res.status === 400 ){
            return [ res.status, await res.json()]
        } else{
            // unrecognized error, JSON may not be available
            return [ res.status, await res.text()]
        }
    }

    // check if we have json which we should have
    const data = await res.json()

    return [ res.status, data ]
}

export {
    goodChatFileUpload,
    readFileToText,
    apiJSONFetch
}