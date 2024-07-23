import {useState, useEffect} from "react"

function App() {

  const [state, setState]= useState(null);
  const [url, setUrl] = useState("http://localhost:8000/products/?page=1")

  useEffect(() => {
    const response = fetch(url)
    .then(res => res.json())
    .then(json => {
      setState(json);
    })
    .catch(res => console.log(res))


  },[url])

  return (
    <>
    <div className="App">
      {state && JSON.stringify(state['results'])}
    </div>
    {
      ((state!=null && state['next']!=null)) && 
      <button onClick={()=>{setUrl(state['next'])}}>{"Next"}</button>
    }
    {
      ((state!=null && state['previous']!=null)) && 
      <button onClick={()=>{setUrl(state['previous'])}}>{"Prev"}</button>
    }
    </>

  );
}

export default App;
