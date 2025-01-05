import { useState, useEffect } from "react";
import {Cookies, useCookies} from "react-cookie"
import {NotAuthenticated, useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import { useNavigate } from "react-router-dom";
import { getHeaders } from "../utils";

export function LogInView(){

    const {user, isAuthenticated, login, logout} = useAuth()
    const navigate = useNavigate()

    const [formData, setFormData] = useState({
        'username' : "",
        "password" : ""
    })

    const [cookies,setCookies] = useCookies()

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
        ).then(async (response) => {
                const json = await response.json()
                if (response.status===200){
                    login(json.customer)
                    navigate("/")
                    
                    // alert("CSRF: " + cookies.get("csrftoken")+", SESSION: " + cookies.get("sessionid"))
                }else if (response.status===401){
                    alert(json['detail'])
                }else{
                    alert("Something went wrong")
                }
            }
        )
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