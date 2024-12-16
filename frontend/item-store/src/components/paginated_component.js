import {useState, useEffect} from "react"
import { useCookies } from "react-cookie";
import { formatter } from "../utils";

function PaginatedView({endpoint,item,msg}){

    const [state, setState]= useState(null);
    const [url, setUrl] = useState(endpoint)

    const [cookies,setCookies] = useCookies()
  
    useEffect(() => {
      const response = fetch(url,             {
        "method" : "GET",
        mode : "cors",
        headers : {
            "Content-Type" : 'application/json; charset=UTF-8',
            "Access-Control-Allow-Credentials" : true,
            "X-CSRFToken" : cookies.csrftoken
        },
        credentials : "include"
    })
      .then(res => res.json())
      .then(json => {
        console.log(json)
        setState(json);
      })
      .catch(res => console.log(res))
  
  
    },[url,msg])

    if (state!=null){
        console.log(state['results'])

    }

    return (
        <>
        {state && ('total' in state) && <h1>Total: {formatter.format(state.total)}</h1>}
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