import { useState} from "react";
import {NotAuthenticated, useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import { useNavigate } from "react-router-dom";
import { getHeaders } from "../utils";

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

    async function handleSubmit(event){
        event.preventDefault();
        fetch(url+"/customers/register/",
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
        ).then(async (response) => {
            if (!response.ok){
                return Promise.reject(response)
            }
            return response.json()
        }).then(async (json) => {
                // const json = await response.json()
                // if (response.status===200){
                login(json.user)
                navigate("/")
                    
                //     // alert("CSRF: " + cookies.get("csrftoken")+", SESSION: " + cookies.get("sessionid"))
                // }
        }).catch(async (response) => {
            console.log(response)
            const json = await response.json()
            let errors = []
            for (let key in json){
                console.log(json[key])
                errors = errors.concat(json[key])

            }
            console.log(errors)
            setMessage(errors)

        })
    }
        
    const handleChange = (event) => {
        event.preventDefault()
        setFormData(values => ({...formData,[event.target.name] : event.target.value}))
    }


    return (
        <NotAuthenticated>
            <form onSubmit={handleSubmit}>
                <label htmlFor="uname"><b>Username</b></label>
                <input type="text" placeholder="Enter Username" name="username" onChange={handleChange}/>

                <label htmlFor="uname"><b>E-mail</b></label>
                <input type="text" placeholder="Enter E-mail" name="email" onChange={handleChange}/>

                <label htmlFor="password"><b>Password</b></label>
                <input type="password" placeholder="Enter Password" name="password" onChange={handleChange}/>

                <label htmlFor="confirm-password"><b>Confirm Password</b></label>
                <input type="password" placeholder="Confirm Password" name="password2" onChange={handleChange}/>

                <button type="submit">Sign Up</button>
            </form>
            {
                message.map(
                    (error,index) => <p key={index}>{error}</p>
                )
            }
        </NotAuthenticated>
    )
}