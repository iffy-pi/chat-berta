import loading_gif from '../../../media/loading_gif_2.gif'

const SummaryContentLoading = () => {

    return (
        <div className='loading-page'>
            <div className='loading-inner-div'>
                <p className="loading-title">Making Summary...</p>
                <img src={loading_gif} alt="logo" className="loading-image"/>
            </div>
        </div>
    )
}

export default SummaryContentLoading