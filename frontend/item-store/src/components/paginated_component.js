import {useState, useEffect} from "react"
import { useCookies } from "react-cookie";
import { formatter } from "../utils";
import { ErrorView } from "./errorView";
import Button from 'react-bootstrap/Button'
import { getHeaders } from "../utils";

function PaginatedView({endpoint,item,msg}){

    const [state, setState]= useState(null);
    const [url, setUrl] = useState(endpoint)
    const [error,setError] = useState(null)

    const [cookies,setCookies] = useCookies()
  
    useEffect(() => {
      const response = fetch(url,             {
        "method" : "GET",
        mode : "cors",
        headers : getHeaders(),
        credentials : "include"
    }).then(async res => {
        const body = await res.json()
        if (res.status === 200){
          setState(body)
        }else{
          setError(body)
        }
      })
  
    },[url,msg])


    if (error !== null){
      return <ErrorView message={error['detail']}/>
    }


    return (
        <>
        {state && ('total' in state) && <h1>Total: {formatter.format(state.total)}</h1>}
        <div className="App">
          {state && 
          state['results'].map(
            (display_item,index) => item(index,display_item)
            )
          }
        </div>
        {
          ((state!=null && state['previous']!=null)) && 
          <Button className='' onClick={()=>{setUrl(state['previous'])}}>{"Prev"}</Button>
        }
        {
          ((state!=null && state['next']!=null)) && 
          <Button onClick={()=>{setUrl(state['next'])}}>{"Next"}</Button>
        }
        </>
    );
}

export default PaginatedView