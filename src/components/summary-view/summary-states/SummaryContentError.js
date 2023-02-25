import error_icon from '../../../media/error_icon.png'
const SummaryContentError = ({ message }) => {
    return (
        <div className='error-page'>
            <div className='error-inner-div'>
                <div>
                    <img src={error_icon} alt="Error Icon" className="error-image"/>
                </div>
                <div>
                    <p className="error-title">Something went wrong.</p>
                    <p className="error-message">Please try again.</p>
                    <p className="error-message">Error:</p>
                    <p className="error-message">{message}</p>
                </div>
            </div>
        </div>
    )
}

export default SummaryContentError;
