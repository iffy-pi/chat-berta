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

/*
    Returns a Response object for a given API call, repsonse object is of the format:
    {
        success: true or false based on result of call
        status: http status for the call
        content: contains JSON for success call or client side error call, contains text for other failures
    }
*/
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

    const response = {
        success: true,
        status: res.status
    }

    if ( res.status !== 200 ){
        // check if it is a client side error, api always returns 400,
        // if it is then we can return the JSON message
        response.success = false

        response.content = ( res.status === 400) ? await res.json() : await res.text()
        return response
    }

    // check if we have json which we should have
    response.content = await res.json()

    return response
}

// Parse the text into the json format
const chatTextToChatJSON = ( transcriptText ) => {
    const lines = transcriptText.split('\n')

    const parties = []
    const messages = []
    let partiesFound = null
    let curParty = null
    let curPartyID = -1

    for ( let i=0; i < lines.length; i++ ) {
        const line = lines[i]
        if ( line === '' ) continue;

        // get the party that sent the message if it is a party identifier line
        partiesFound = line.match(/^[a-zA-z][a-zA-z]*:/) 
        if ( partiesFound != null  ) {
            // Removing colon from party name
            curParty = partiesFound[0].substring(0, partiesFound[0].length-1)

            curPartyID = parties.indexOf(curParty)

            if ( curPartyID === -1 ) {
                curPartyID = parties.length
                parties.push(curParty)
            }
            continue;
        }

        if ( curPartyID === -1) throw new Error('No party labels found!')

        // Add to messages if it is not already present
        messages.push({
            id: messages.length,
            pid: curPartyID,
            text: line
        })
        
    }

    if ( messages.length === 0 ) throw new Error('No messages found in the transcript!')

    // if ( parties.length > 2 ) throw new Error('Chat summarization is only supported for two parties!')

    const partiesObj = []
    parties.forEach((p, i) => { partiesObj.push({ id: i, name: p })})

    const parsedChat = {
        config: {
            parties: partiesObj
        },
        messages: messages
    }

    return parsedChat

}

export {
    goodChatFileUpload,
    readFileToText,
    apiJSONFetch,
    chatTextToChatJSON
}