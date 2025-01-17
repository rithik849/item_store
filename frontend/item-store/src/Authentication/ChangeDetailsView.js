import {useState} from "react"
import {useAuth, Authenticated} from "../components/is_authenticated_component"
import {url} from "../constants"
import {getHeaders} from "../utils"

export function ChangeDetailsView(){

    const {user, update} = useAuth()

    const [message, setMessage] = useState([])

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
            update(formData)
        }catch (error){
            console.error(error)
            if (json !== undefined){
                let error_messages = ""
                for (let key in json.detail){
                    error_messages += json.detail[key]

                }
                setMessage(error_messages.split("."))
            }
        }

        // fetch(url+"/customers/change-details/",
        //     {
        //         method : "POST",
        //         mode : 'cors',
        //         headers : getHeaders(),
        //         credentials : "include",
        //         body : JSON.stringify({
        //             "username" : formData.username,
        //             "email" : formData.email
        //         })
        //     }
        // ).then((response) => {
        //     if (!response.ok){
        //         return Promise.reject(response)
        //     }
        //     return response.json()
        // }).then((json) => {
        //     // if (response.status===200){
        //     setMessage([json.detail])
        //     update(formData)
        //     // }else if (response.status===400){
        //     //     let errors = ""
        //     //     for (let key in json.detail){
        //     //         errors += json.detail[key]

        //     //     }
        //     //     setMessage(errors.split("."))
        //     // }
        // }).catch(async (response) => {
        //     if (response.headers.get("content-type") === "application/json"){
        //         let json = await response.json()
        //         let errors = ""
        //         for (let key in json.detail){
        //             errors += json.detail[key]

        //         }
        //         setMessage(errors.split("."))
        //     }
        // })
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