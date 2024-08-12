import {Cookies, useCookies} from "react-cookie"
import { useEffect, useState } from "react"
import { useAuth, Authenticated } from "../components/is_authenticated_component"

export function ProfileView(){

    const {user, isAuthenticated, login, logout} = useAuth()

    const [formData, setFormData] = useState({
        '' : "",
        '' : ""
    })
    const [message, setMessage] = useState([])

    return ( 
        <Authenticated>
            {isAuthenticated && 
                <>
                    <div>
                        {user.username}
                    </div>
                    <div>
                        {user.email}
                    </div>
                </>
            }
        </Authenticated>
    )
}