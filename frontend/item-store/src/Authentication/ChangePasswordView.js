import {useState } from "react"
import { useAuth, Authenticated } from "../components/is_authenticated_component"
import {url} from "../constants"
import { getHeaders, process_errors } from "../utils"
import { DisplayMessage } from "../components/errorView"

export function ChangePasswordView(){

    const {isAuthenticated} = useAuth()

    const [formData, setFormData] = useState({
        'password' : "",
        "confirm_password" : ""
    })
    const [message, setMessage] = useState([])
    const [isError, setError] = useState(false)


    async function handleSubmit(event){
        event.preventDefault();
        let response
        let json
        try{
            response = await fetch(url+"/customers/change-password/",
                {
                    method : "PATCH",
                    mode : 'cors',
                    headers : getHeaders(),
                    credentials : "include",
                    body : JSON.stringify({
                        "password" : formData.password,
                        "confirm_password" : formData.confirm_password
                    })
                }
            )
            json = await response.json()
            if (!response.ok){
                throw Error('Something went wrong')
            }
            setMessage([json.detail])
            setError(false)
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
        <Authenticated>
            {isAuthenticated && 
            <>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="uname"><b>Password</b></label>
                    <input type="password" placeholder="Enter Password" name="password" onChange={handleChange}/>

                    <label htmlFor="email"><b>Confirm Password</b></label>
                    <input type="password" placeholder="Confirm Password" name="confirm_password" onChange={handleChange}/>

                    <button type="submit">Change Password</button>
                </form>
                <div className={isError ? 'text-danger' : 'text-success'}>
                    <DisplayMessage messages={message}/>
                </div>
            </>}
        </Authenticated>
    )
}