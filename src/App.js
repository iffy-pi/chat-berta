import Header from './components/Header'
import { useState, useEffect } from 'react'
import Button from './components/Button';
import { SERVER_BACKEND } from './configs/apiconfig'

// Note that server back end uses the root directory just like flask
// So now we handle api requests by adding the api route
// const SERVER_BACKEND = 'http://127.0.0.1:5000/api'

function App() {

  const [ headerMsg, setHeaderMsg ] = useState('Hello World!')
  const [ btnToggle, setButtonToggle ] = useState(true)

  const toggleButton = () => {
    setButtonToggle(!btnToggle)
    setHeaderMsg(btnToggle ? "Hello World!" : "Goodbye World :(")
  }

  const getBEMsg = async () => {
    setHeaderMsg('Querying...')
    const res = await fetch (
      `${SERVER_BACKEND}/react-testing`,
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

  useEffect( () => {
    //getBEMsg()
  }, [])


  return (
    <div>
      <Header message={headerMsg}/>
      <Button buttonText="Click?" onClick={toggleButton}/>
      <Button buttonText="Query Backend" onClick={getBEMsg}/>
    </div>
  );
}

export default App;
