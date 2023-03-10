import { useState } from 'react'
import ControlBoard from './components/control-board/ControlBoard';
import SummaryView from './components/summary-view/SummaryView';
import { ContentStates } from './functions/basefunctions';

function App() {  
  const [ summaryResponse , setSummaryResponse ] = useState({
        contentState: ContentStates.unset,
        success: false, // Whether the response worked
        body: null, // actual server response
        error: '' // Used if there are any errors
  })

  /*
    summaryRequest is object of properties to make a summary with
    request is populated from SubmitChat and used in the summary view

    summaryResponse is the server response to the summary request
    the response is made in the SubmitChat component, at the click of the summarize button
    Is populated with the server response, and any other error information needed by summary view
  */


  return (
    <div className="">
      <div className="app-container">
        <ControlBoard summaryResponse={summaryResponse} setSummaryResponse={setSummaryResponse}/>
        <SummaryView summaryResponse={summaryResponse}/>
      </div>
    </div>
  );
}

export default App;

// Sample comment 
