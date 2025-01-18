import { useState} from "react";
import {NotAuthenticated, useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import { useNavigate } from "react-router-dom";
import { getHeaders, process_errors } from "../utils";
import { DisplayMessage } from "../components/errorView";

export function SignUpView(){

    const {login} = useAuth()
    const navigate = useNavigate()

    const [formData, setFormData] = useState({
        "username" : "",
        "email" : "",
        "password" : "",
        "password2" : ""
    })

    const [message,setMessage] = useState([])
    const [isError, setError] = useState(false)

    async function handleSubmit(event){
        event.preventDefault();
        let response
        let json
        try{
            response = await fetch(url+"/customers/register/",
                {
                    method : "POST",
                    mode : 'cors',
                    headers : getHeaders(),
                    credentials : "include",
                    body : JSON.stringify({
                        "username" : formData.username,
                        "email" : formData.email,
                        "password" : formData.password,
                        "password2" : formData.password2
                    })
                }
            )

            json = await response.json()
            if (!response.ok){
                throw Error('Something went wrong')
            }
            login(json.user)
            navigate("/")

        }catch (error){
            console.error(error)
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


    return (
        <NotAuthenticated>
            <form className="d-flex justify-content-center" onSubmit={handleSubmit}>
                <div className="d-flex p-2 justify-content-center align-items-center flex-column bg-secondary text-white w-50 rounded">
                    <label htmlFor="uname"><b>Username</b></label>
                    <input type="text" placeholder="Enter Username" name="username" onChange={handleChange}/>

                    <label htmlFor="uname"><b>E-mail</b></label>
                    <input type="text" placeholder="Enter E-mail" name="email" onChange={handleChange}/>

                    <label htmlFor="password"><b>Password</b></label>
                    <input type="password" placeholder="Enter Password" name="password" onChange={handleChange}/>

                    <label htmlFor="confirm-password"><b>Confirm Password</b></label>
                    <input type="password" placeholder="Confirm Password" name="password2" onChange={handleChange}/>

                    <button className={"btn mt-4"} type="submit">Sign Up</button>
                    
                    <div className={"border border-secondary rounded " + (isError ? 'text-danger' : 'text-success')}>
                        <DisplayMessage messages={message}/>
                    </div>
                </div>
            </form>
        </NotAuthenticated>
    )
}