import {Cookies, useCookies} from "react-cookie"
import { useEffect, useState } from "react"
import { useAuth, Authenticated } from "../components/is_authenticated_component"
import {url} from "../constants"

export function ChangeDetailsView(){

    const {user, isAuthenticated, login, logout} = useAuth()

    const [message, setMessage] = useState([])

    const [formData, setFormData] = useState({
        'username' : "",
        "email" : ""
    })

    const [cookies,setCookies] = useCookies()

    useEffect(()=>{
        if (user!==null){
            
            setFormData(values => ({...formData,'username' : user.username,'email' : user.email}))
        }
    },[user])

    async function handleSubmit(event){
        event.preventDefault();
        fetch(url+"/customers/change-details/",
            {
                method : "POST",
                mode : 'cors',
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include",
                body : JSON.stringify({
                    "username" : formData.username,
                    "email" : formData.email
                })
            }
        ).then(async (response) => {
            const json = await response.json()
                if (response.status==200){
                    setMessage([json.detail])
                }else if (response.status==400){
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
            { user &&
            <>
                <form onSubmit={handleSubmit}>
                    <label htmlFor="uname"><b>Username</b></label>
                    <input type="text" placeholder="Enter Username" name="username" onChange={handleChange} value={formData.username}/>

                    <label htmlFor="email"><b>Email</b></label>
                    <input type="email" placeholder="Enter Email" name="email" onChange={handleChange} value={formData.email}/>

                    <button type="submit">Change Details</button>
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