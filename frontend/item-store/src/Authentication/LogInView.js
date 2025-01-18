import { useState} from "react";
import {NotAuthenticated, useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import { useNavigate } from "react-router-dom";
import { getHeaders, process_errors } from "../utils";
import { useCookies } from "react-cookie";
import { DisplayMessage } from "../components/errorView";

export function LogInView(){

    const {login} = useAuth()
    const navigate = useNavigate()


    const [formData, setFormData] = useState({
        'username' : "",
        "password" : ""
    })

    const [message, setMessage] = useState([])
    const [isError,setError] = useState(false)

    async function handleSubmit(event){
        event.preventDefault();
        let json
        let response
        try{
            response = await fetch(url+"/customers/login/",
                {
                    method : "POST",
                    mode : 'cors',
                    headers : getHeaders(),
                    credentials : "include",
                    body : JSON.stringify({
                        "username" : formData.username,
                        "password" : formData.password
                    })
                }
            )

            json = await response.json()
            if (!response.ok){
                throw Error('There was a problem')
            }
            login(json.customer)
            navigate("/")
            
        }catch (error){
            console.error(response)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(true)
            }
        }
    }
        
        const handleChange = (event) => {
        event.preventDefault()
        setFormData(values => ({...formData,[event.target.name] : event.target.value}))


    }

    console.log("RENDER LOGIN")

    return (
        <NotAuthenticated>
            <form onSubmit={handleSubmit}>
                <label htmlFor="uname"><b>Username</b></label>
                <input type="text" placeholder="Enter Username" name="username" onChange={handleChange}/>

                <label htmlFor="psw"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="password" onChange={handleChange}/>

                <button type="submit">Login</button>
            </form>
            <div className={isError ? "text-danger" : 'text-success'}>
                <DisplayMessage messages={message}/>
            </div>
        </NotAuthenticated>
    )
}