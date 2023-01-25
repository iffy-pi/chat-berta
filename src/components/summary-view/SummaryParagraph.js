import { useEffect, useState } from "react"
import Button from "../common/Button"

const SummaryParagraph = ({ chatPackage, characterLimit }) => {
    // Compile all the sentences in the summary messages into one paragraph

    const [ paragraphLimited, setParagraphLimited ] = useState(true)


    const endsWithPunctuation = ( sentence ) => {
        // Checks if the sentence ends with punctuation
        const punctuations = ".?!,;"

        for( const punc of punctuations.split("") ) {
            if ( sentence.endsWith(punc) ) return true
        }
        return false
    }

    const collateMessages = ( summaryMessages ) => {
        let summaryParagraph = ''
        let sentence = ''
        for ( const message of summaryMessages ) {
            // Add punctuation if missing
            sentence = ( !endsWithPunctuation(message.text) ) ? message.text + "." : message.text
            // Append to summary paragraph
            summaryParagraph = ( summaryParagraph === '' ) ? sentence : summaryParagraph + ' ' + sentence
        }

        return summaryParagraph
    }

    const truncateParagraph = ( paragraph ) => {
        // truncate the paragraph based on our specified character limit
        // if paragraph is not limited, then dont do truncate
        if ( !paragraphLimited || characterLimit <= 0 ) return paragraph

        // No truncation required if paragraph is less than limit
        if ( paragraph.length <= characterLimit ) return paragraph

        // Truncate the paragraph to also have space to include elipses
        return (paragraph.substring(0, characterLimit-3) + '...')
        

    }

    const toggleParagraphTruncation = ( ) => {
        setParagraphLimited( !paragraphLimited )
    }

    return (
        <div className="basic-container">
            <h3>Summary Paragraph</h3>
            <div className="basic-container">
                <p>{truncateParagraph(collateMessages(chatPackage.summary_messages)) }</p>
            </div>
            <Button buttonText={ (paragraphLimited) ? "See Full Paragraph" : "Show Less" } onClick={ toggleParagraphTruncation }/>
        </div>
    )
}

SummaryParagraph.defaultProps = {
    characterLimit: 50 // maximum number of characters shown by default in the summary
}

export default SummaryParagraph

