import {useState } from "react"
import { useAuth, Authenticated } from "../components/is_authenticated_component"
import {url} from "../constants"
import { getHeaders } from "../utils"

export function ChangePasswordView(){

    const {isAuthenticated} = useAuth()

    const [formData, setFormData] = useState({
        'password' : "",
        "confirm_password" : ""
    })
    const [message, setMessage] = useState([])


    async function handleSubmit(event){
        event.preventDefault();
        fetch(url+"/customers/change-password/",
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
        ).then((response) => {
            if (!response.ok){
                return Promise.reject(response)
            }
            return response.json()
        }).then((json) => {
            setMessage([json.detail])
        }).catch(async (response) => {
            if (response.headers.get("content-type") === "application/json"){
                let json = await response.json()
                let errors = ""
                for (let key in json.detail){
                    errors += json.detail[key]

                }
                setMessage(errors.split("."))
            }
        })
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
                <div>
                {
                message.map(
                    (error,index) => <p key={index}>{error}</p>
                )
                }
                </div>
            </>}
        </Authenticated>
    )
}