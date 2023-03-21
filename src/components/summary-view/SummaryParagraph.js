import { useState, useEffect } from "react"
import Button from "../common/Button"

const SummaryParagraph = ({ chatPackage, characterLimit }) => {
    // Compile all the sentences in the summary messages into one paragraph
    
    // Holds the summary messages made into a paragraph
    const [ fullParagraph, setFullParagraph ] = useState('')

    // Indicates if the display paragraph is truncated
    // Truncated by default
    const [ displayPargTruncated, setDisplayPargTruncated ] = useState(true)
    
    const needsTruncation = (paragraph) => {
        return paragraph.length > characterLimit
    }

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

    const toggleParagraphTruncation = ( ) => {
        setDisplayPargTruncated( !displayPargTruncated)
    }

    const getDisplayParagraph = () => {
        if ( !needsTruncation(fullParagraph) ) return fullParagraph;

        // Needs truncation and should be truncated
        if ( displayPargTruncated ) return (fullParagraph.substring(0, characterLimit-3) + '...')

        // needs truncation but should not be truncated
        return fullParagraph;
    }

    useEffect(  () => {
        // on receiving the chat package we want to rerender our display information
        if ( chatPackage !== null ) {
            // Paragraph is now included in the summary package
            setFullParagraph(chatPackage.summary.paragraph)
        }
    }, [ chatPackage ])

    return (
        <div className="summary-paragraph">
            <h2>Summary Paragraph</h2>
            <div className="">
                <p>{getDisplayParagraph()}</p>
            </div>
            {
                ( needsTruncation(fullParagraph) ) &&
                <div className="sp-btn-div">
                    <Button buttonText={ (displayPargTruncated) ? "Show All" : "Show Less" } onClick={ toggleParagraphTruncation }/>
                </div>   
            }
        </div>
    )
}

SummaryParagraph.defaultProps = {
    characterLimit: 50 // maximum number of characters shown by default in the summary
}

export default SummaryParagraph

