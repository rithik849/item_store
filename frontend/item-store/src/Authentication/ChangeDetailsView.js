import {useState} from "react"
import {useAuth, Authenticated} from "../components/is_authenticated_component"
import {url} from "../constants"
import {getHeaders, process_errors} from "../utils"
import { DisplayMessage } from "../components/errorView"

export function ChangeDetailsView(){

    const {user, update} = useAuth()

    const [message, setMessage] = useState([])
    const [isError, setError] = useState(false)

    const [formData, setFormData] = useState({
        'username' : user==null ? "" : user.username,
        "email" : user===null ? "" : user.email
    })

    async function handleSubmit(event){
        event.preventDefault();
        let response
        let json
        try{
            response = await fetch(url+"/customers/change-details/",
                {
                    method : "POST",
                    mode : 'cors',
                    headers : getHeaders(),
                    credentials : "include",
                    body : JSON.stringify({
                        "username" : formData.username,
                        "email" : formData.email
                    })
                }
            )
            json = await response.json()
            if (!response.ok){
                throw Error('Something went wrong')
            }
            setMessage([json.detail])
            setError(false)
            update(formData)
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
        setFormData(data => ({...data, [event.target.name] : event.target.value}))
    }

    return (
        <Authenticated>
            { user &&
            <>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="uname"><b>Username</b></label>
                    <input type="text" placeholder="Enter Username" name="username" onChange={handleChange} value={formData.username}/>

                    <label htmlFor="email"><b>Email</b></label>
                    <input type="email" placeholder="Enter Email" name="email" onChange={handleChange} value={formData.email}/>

                    <button type="submit">Change Details</button>
                </form>
                <div className={isError ? 'text-danger' : "text-success"}>
                    <DisplayMessage messages={message}/>
                </div>
            </>}
        </Authenticated>
    )
}