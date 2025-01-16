import { useState} from "react";
import {NotAuthenticated, useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import { useNavigate } from "react-router-dom";
import { getHeaders } from "../utils";
import { useCookies } from "react-cookie";

export function LogInView(){

    const {login} = useAuth()
    const navigate = useNavigate()


    const [formData, setFormData] = useState({
        'username' : "",
        "password" : ""
    })

    async function handleSubmit(event){
        event.preventDefault();
        fetch(url+"/customers/login/",
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
        ).then((response) => {
            if (!response.ok){
                return Promise.reject(response)
            }

            return response.json()
        }).then((json) => {
                console.log(json)
                login(json.customer)
                navigate("/")
        }).catch(async (response) => {
            if (response.headers.get('content-type') === 'application/json'){
                let json = await response.json()
                alert(json['detail'])
            }
            console.error(response)
        })
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
        </NotAuthenticated>
    )
}