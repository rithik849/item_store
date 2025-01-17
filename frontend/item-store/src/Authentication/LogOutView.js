import { useNavigate } from "react-router-dom"
import { Authenticated } from "../components/is_authenticated_component"
import { useAuth } from "../components/is_authenticated_component"

export function LogOutView(){

    const {logout} = useAuth()
    const nav = useNavigate()

    function handleSubmit(event){
        event.preventDefault()
        logout()
        nav("/",{replace:true})
    }

    return(
        <Authenticated>
        { 
            <div>
                <button onClick= {handleSubmit}>{"Log Out"}</button>
            </div>
        }
        </Authenticated>
    )
}