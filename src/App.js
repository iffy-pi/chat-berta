import { useState } from 'react'
import ControlBoard from './components/control-board/ControlBoard';
import SummaryView from './components/summary-view/SummaryView';

function App() {  
  const [ summaryRequest, setSummaryRequest ] = useState(null)

  /*
    summaryRequest is object of properties to make a summary with
    request is populated from SubmitChat and used in the summary view
  */


  return (
    <div>
      <ControlBoard setSummaryRequest={setSummaryRequest}/>
      <SummaryView summaryRequest={summaryRequest}/>
    </div>
  );
}

export default App;
