import { useState } from 'react'
import ControlBoard from './components/control-board/ControlBoard';
import SummaryView from './components/summary-view/SummaryView';

function App() {  
  const [ summaryRequest, setSummaryRequest ] = useState(null)
  const [ summaryResponse , setSummaryResponse ] = useState(null)

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
        <ControlBoard setSummaryRequest={setSummaryRequest} setSummaryResponse={setSummaryResponse}/>
        <SummaryView summaryRequest={summaryRequest} summaryResponse={summaryResponse}/>
      </div>
    </div>
  );
}

export default App;

// Sample comment 
