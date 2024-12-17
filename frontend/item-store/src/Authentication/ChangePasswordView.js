import {Cookies, useCookies} from "react-cookie"
import { useEffect, useState } from "react"
import { useAuth, Authenticated } from "../components/is_authenticated_component"
import {url} from "../constants"

export function ChangePasswordView(){

    const {user, isAuthenticated, login, logout} = useAuth()

    const [formData, setFormData] = useState({
        'password' : "",
        "confirm_password" : ""
    })
    const [message, setMessage] = useState([])

    const [cookies,setCookies] = useCookies()

    async function handleSubmit(event){
        event.preventDefault();
        fetch(url+"/customers/change-password/",
            {
                method : "PATCH",
                mode : 'cors',
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include",
                body : JSON.stringify({
                    "password" : formData.password,
                    "confirm_password" : formData.confirm_password
                })
            }
        ).then(async (response) => {
            const json = await response.json()
                if (response.status===200){
                    setMessage([json.detail])
                }else if (response.status===400){
                    let errors = ""
                    for (let key in json.detail){
                        errors += json.detail[key]

                    }
                    setMessage(errors.split("."))
                }
            }
        )
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