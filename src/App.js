import Header from './components/Header'
import { useState, useEffect } from 'react'
import Button from './components/Button';

// Note that server back end uses the root directory just like flask
// So now we handle api requests by adding the api route
const SERVER_BACKEND = '/api'

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

    console.log(res)
    
    if (res.status !== 200) {
      setHeaderMsg('Failed to get message!')
      return
    }


    // Get json is failing becasue flask is autowrappign the return content in html
    // Which is failing to parse, need to find some way to reconfigure the response
    const data = await res.json()

    console.log(data)
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
