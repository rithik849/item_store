import {useState, useEffect, useLayoutEffect, useRef, useMemo, useContext, createContext} from "react"
import { ErrorView } from "./errorView"
import {Cookies, useCookies} from "react-cookie"
import {url} from "../constants"
import { getHeaders } from "../utils";

const AuthContext = createContext();
export const AuthProvider = (props) => {
    const [user, setUser] = useState(props.user)
    const [isAuthenticated, setAuthenticated] = useState(props.isAuthenticated)
    const [cookies, setCookies] = useCookies()
    
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
        fetch(url+"/customers/logout/",
            {
                method:"POST",
                mode : 'cors',
                headers : getHeaders(),
                credentials:"include",
            }
        ).then(request =>{
            if (request.status===200){
                setUser({'username':"",'email':""})
                setAuthenticated(false)
                const obj = new Cookies()
                obj.remove('csrftoken')
            }
        }
        )
        
    }
  
    const value = useMemo(
      () => ({
        user,
        isAuthenticated,
        login,
        logout,
        update
      }),
      [user]
    )

    return <AuthContext.Provider value={value}>{props.children}</AuthContext.Provider>;
  };

export function useAuth(){
    const auth = useContext(AuthContext)
    return auth
}

export function Authenticated(props){

    const {user, isAuthenticated, login, logout} = useAuth()

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
    const {user, isAuthenticated, login, logout} = useAuth()

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
