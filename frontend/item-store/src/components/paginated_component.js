import {useState, useEffect} from "react"
import { formatter } from "../utils";
import { ErrorView } from "./errorView";
import Button from 'react-bootstrap/Button'
import { getHeaders } from "../utils";

function PaginatedView({endpoint,item,msg,displayClass}){

    const [state, setState]= useState(null);
    const [url, setUrl] = useState(endpoint)
    const [error,setError] = useState(null)

  
    useEffect(() => {
        fetch(url,{
            method : "GET",
            mode : "cors",
            headers : getHeaders(),
            credentials : "include"
        }).then( response => {
            // Check if response is ok
            if (!response.ok){
                return Promise.reject(response)
            }

            return response.json()
        }).then(async json => {
            setState(json)
        }).catch(
            async (error) => {
                console.log(error.headers.get('content-type'))
                if (error.headers.get('content-type') === "application/json"){
                    console.log('HERE')
                    const json_error = await error.json()
                    setError(json_error)
                }else{
                    setError(error)
                }
        }
      )
  
    },[url,msg])


    if (error !== null){
        console.error(error)
        if ('detail' in error){
            return <ErrorView message={error['detail']}/>
        }
        return <ErrorView message={error.toString()}/>
    }


    return (
        <>
        {(state && ('total' in state)) ? <h1>Total: {formatter.format(state.total)}</h1> : ""}
        <div className={displayClass}>
          {state ? 
          state['results'].map(
            (display_item,index) => item(index,display_item)
            ) : ""
          }
        </div>
        <div className= "d-flex justify-content-center btn-group pt-5" role="group">
          {
            ((state!=null && state['previous']!=null)) ? 
            <Button type="button" className='btn btn-primary' onClick={()=>{setUrl(state['previous'])}}>{"Prev"}</Button> : 
            ""
          }
          {
            ((state!=null && state['next']!=null)) ?
            <Button className='btn btn-primary' onClick={()=>{setUrl(state['next'])}}>{"Next"}</Button> :
            ""
          }
        </div>
        </>
    );
}

export default PaginatedView