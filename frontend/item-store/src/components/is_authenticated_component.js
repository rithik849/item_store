import {useState, useMemo, useContext, createContext} from "react"
import { ErrorView } from "./errorView"
import {Cookies} from "react-cookie"
import {url} from "../constants"
import { getHeaders } from "../utils";

const AuthContext = createContext();
export const AuthProvider = (props) => {
    const [user, setUser] = useState(props.user)
    const [isAuthenticated, setAuthenticated] = useState(props.isAuthenticated)
    
    // call this function when you want to authenticate the user
    const login = (data) => {
        setUser(data)
        setAuthenticated(true)
        // setUser(data)
    }

    const update = (data) => {
        setUser(prev => ({...prev,...data}))
    }
  
    // call this function to sign out logged in user
    const logout = () => {

        let fetchLogOut = async () => {
            let response
            response = await fetch(url+"/customers/logout/",
                {
                    method:"POST",
                    mode : 'cors',
                    headers : getHeaders(),
                    credentials:"include",
                }
            )
            if (!response.ok){
                console.log(response)
                throw Error('There was a problem')
            }
            setUser({'username':"",'email':""})
            setAuthenticated(false)
            const obj = new Cookies()
            obj.remove('csrftoken')
            obj.remove('sessionid')
        }

        fetchLogOut().catch(error => console.error(error))
        
    }
  
    const value = useMemo(
      () => ({
        user,
        isAuthenticated,
        login,
        logout,
        update
      }),
      [user,isAuthenticated]
    )

    return <AuthContext.Provider value={value}>{props.children}</AuthContext.Provider>;
  };

export function useAuth(){
    const auth = useContext(AuthContext)
    return auth
}

export function Authenticated(props){

    const {user, isAuthenticated} = useAuth()

    if ((isAuthenticated===true && user.username!=="")){
        return (props.children)
    }
    if ((isAuthenticated)===false){
        return (
            <ErrorView message= "You must be logged in to access this page."/>
        )
    }

    return (<></>)
}

export function NotAuthenticated(props){
    const {user, isAuthenticated} = useAuth()

    if (isAuthenticated===false && user.username===""){
        return (props.children)
    }
    if(isAuthenticated===true){
        return (
            <ErrorView message= "You are already logged in."/>
        )
    }
    console.log(isAuthenticated,user)
    return (<></>)
}
