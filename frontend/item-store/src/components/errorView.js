import { useEffect } from "react"
import {useNavigate} from "react-router-dom"



export function ErrorView({message}){

    const navigate = useNavigate()

    useEffect(() => {
        setTimeout(() => {
            navigate('/')
        }, 2000)
    },[navigate])

    return (
        <div className='error'>
            <h1>
                {message}
            </h1>
        </div>
    )
}

export function DisplayMessage({messages}){

    return (
        <ul>
        {messages.map((message,idx) => <li key={idx}>{message}</li>)}
        </ul>
    )
}