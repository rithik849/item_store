import {useState, useEffect} from "react"
import Product from "./product_card"


function PaginatedView({endpoint,item}){

    const [state, setState]= useState(null);
    const [url, setUrl] = useState(endpoint)
  
    useEffect(() => {
      const response = fetch(url)
      .then(res => res.json())
      .then(json => {
        setState(json);
      })
      .catch(res => console.log(res))
  
  
    },[url])

    if (state!=null){
        console.log(state['results'])

    }

    return (
        <>
        <div className="App">
          {state && 
          state['results'].map(
            (display_item,index) => item(index,display_item)
        )}
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

export default PaginatedView