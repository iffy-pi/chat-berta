import { useState, useEffect } from "react"
import Button from "../common/Button"

const SummaryParagraph = ({ chatPackage, characterLimit }) => {
    // Compile all the sentences in the summary messages into one paragraph

    // Used to indicate if the displayed paragraph is limited or not
    const [ displayParagraphLimited, setDisplayParagraphLimited ] = useState(true)
    
    // Holds the summary messages made into a paragraph
    const [ fullParagraph, setFullParagraph ] = useState('')
    
    // Indicates if the paragraph will need truncation
    const [ needsTruncation, setNeedsTruncation ] = useState(false)

    // Indicates if the display paragraph is truncated
    // Truncated by default
    const [ shouldTruncateParagraph, setShouldTruncateParagaph ] = useState(true)
    


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
        if ( !displayParagraphLimited || characterLimit <= 0 ) return paragraph

        // No truncation required if paragraph is less than limit
        if ( paragraph.length <= characterLimit ) return paragraph

        // Truncate the paragraph to also have space to include elipses
        return (paragraph.substring(0, characterLimit-3) + '...')
        

    }

    const toggleParagraphTruncation = ( ) => {
        setShouldTruncateParagaph( !shouldTruncateParagraph)
    }

    useEffect(  () => {
        // on receiving the chat package we want to rerender our display information
        if ( chatPackage !== null ) {
            setFullParagraph(collateMessages(chatPackage.summary_messages))
            setNeedsTruncation( fullParagraph.length <= characterLimit )
        }
    }, [ chatPackage ])

    const getDisplayParagraph = () => {
        if ( !needsTruncation ) return fullParagraph;

        // Needs truncation and should be truncated
        if ( shouldTruncateParagraph ) return (fullParagraph.substring(0, characterLimit-3) + '...')

        // needs truncation but should not be truncated
        return fullParagraph;
    }

    return (
        <div className="summary-paragraph">
            <h3>Summary Paragraph</h3>
            <div className="sp-text">
                <p>{getDisplayParagraph()}</p>
            </div>
            <div className="sp-btn-div">
                <Button buttonText={ (shouldTruncateParagraph) ? "See More" : "Show Less" } onClick={ toggleParagraphTruncation }/>
            </div>
        </div>
    )
}

SummaryParagraph.defaultProps = {
    characterLimit: 50 // maximum number of characters shown by default in the summary
}

export default SummaryParagraph

