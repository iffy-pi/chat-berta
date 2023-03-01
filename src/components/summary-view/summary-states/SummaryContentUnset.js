import pic from '../../../media/summary_request.jpg'

const SummaryContentUnset = () => {
    return (
        <div className='loading-page'>
            <div className='loading-inner-div'>
                <img src={pic} alt="logo" className="unset-image"/>
                <p className="unset-title">Submit A Summary Request!</p>
            </div>
        </div>
    )
}

export default SummaryContentUnset;
