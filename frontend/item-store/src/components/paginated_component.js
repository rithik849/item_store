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
        const fetchData = async () => {
            let response
            let json
            response = await fetch(url,{
                method : "GET",
                mode : "cors",
                headers : getHeaders(),
                credentials : "include"
            })
            json = await response.json()
            if (!response.ok){
                throw Error(json)
            }
            setState(json)
        }

        fetchData().catch((err) => {
            setError(err.message)
            console.error(err)
        })  
    },[url,msg])


    if (error !== null){
        if ('detail' in error){
            return <ErrorView message={error['detail']}/>
        }
        return <ErrorView message={error.toString()}/>
    }


    return (
        <>
        {(state && ('total' in state)) ? <h1>Total: {formatter.format(state.total)}</h1> : ""}
        <div className={displayClass}>
            {
                state ? state['results'].map(
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