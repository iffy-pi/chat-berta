import Header from './components/common/Header'
import { useState, useEffect } from 'react'
import Button from './components/common/Button';
import { CHAT_BERTA_API } from './configs/apiconfig'
import ControlBoard from './components/control-board/ControlBoard';
import SummaryView from './components/summary-view/SummaryView';

const summaryStates = {
  undef: 0,
  paramsSent: 1
}

function App() {

  const [ headerMsg, setHeaderMsg ] = useState('Hello World!')
  const [ btnToggle, setButtonToggle ] = useState(true)

  
  const [ summaryRequest, setSummaryRequest ] = useState(null)

  /*
    summaryRequest is object of properties to make a summary with
    request is populated from SubmitChat and used in the summary view
  */

  const toggleButton = () => {
    setButtonToggle(!btnToggle)
    setHeaderMsg(btnToggle ? "Hello World!" : "Goodbye World :(")
  }

  const getBEMsg = async () => {
    setHeaderMsg('Querying...')
    const res = await fetch (
      `${CHAT_BERTA_API}/react-testing`,
    )
    
    console.log('Response:===>')
    console.log(res)
    console.log('End Response:===>')
    console.log('State:====>')
    console.log(`HTTP ${res.status} ${res.statusText}`)
    console.log(`Type: ${res.type}`)
    console.log('End State:====>')
    console.log('Headers:===>')
    res.headers.forEach(function(val, key) { console.log(`'${key}': '${val}'`); })
    console.log(res.headers.get('content-type'))
    console.log('End Headers:===>')
    
    // 201 is testing if we actually connected to the server
    // since api is designed to return code 201
    const serverReached = ( res.status === 201)
    let tempMsg = ''
    if (!serverReached) {
      if ( res.status !== 200 ){
        tempMsg = (`Failure Status Code: ${res.status}`)
      } else {
        tempMsg = 'Did not reach server but got 200 response!'
      }
      setHeaderMsg(tempMsg)
    }

    console.log('Body Text:===>')
    const resText = await res.text()
    console.log(resText)
    console.log('End Body Text:======>')


    // Get json is failing becasue flask is autowrappign the return content in html
    // Which is failing to parse, need to find some way to reconfigure the response
    const data = JSON.parse(resText)
    setHeaderMsg(data.message)
  }


  return (
    <div>
      <Header message={headerMsg}/>
      <Button buttonText="Click?" onClick={toggleButton}/>
      <Button buttonText="Query Backend" onClick={getBEMsg}/>
      <ControlBoard summaryRequest={summaryRequest} setSummaryRequest={setSummaryRequest}/>
      <SummaryView summaryRequest={summaryRequest} setSummaryRequest={setSummaryRequest}/>
    </div>
  );
}

export default App;
