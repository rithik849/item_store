import {useState, useEffect, useLayoutEffect, useRef, useMemo, useContext, createContext} from "react"
import { ErrorView } from "./errorView"
import {Cookies, useCookies} from "react-cookie"

const AuthContext = createContext();
export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [isAuthenticated, setAuthenticated] = useState(null)
    const [cookies, setCookies] = useCookies()

    useEffect(() => {
        console.log("EFFECT MAIN")
        const controller = new AbortController();
        const abort_signal = controller.signal

        fetch("http://localhost:8000/customers/login/",{
            "method":"GET",
            "Content-Type":"application/json",
            "signal":abort_signal,
            "credentials":"include"}
        ).then(async response => {
            if (response.status==200){
                const json = await response.json()
                if (json.is_authenticated===true){
                    console.log(json.customer)
                    setUser(json.customer)
                    setAuthenticated(json.is_authenticated)
                }else{
                    setUser(null)
                    setAuthenticated(false)
                }
            }
        }).catch(
            (err) => {
                console.log(err)
                if (!controller.signal.aborted){
                    console.log("Signal not aborted")

                }
            }
        )
        return () => {controller.abort()}
    },[])


  
    // call this function when you want to authenticate the user
    const login = (data) => {
        setUser(data)
        setAuthenticated(true)
        // setUser(data)
    }
  
    // call this function to sign out logged in user
    const logout = () => {
        fetch("http://localhost:8000/customers/logout/",
            {
                method:"POST",
                credentials:"include",
                mode : 'cors',
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
            }
        ).then(request =>{
            if (request.status===200){
                setUser(null)
                setAuthenticated(false)
            }
        }
        )
        // user.current = null
        
    }
  
    const value = useMemo(
      () => ({
        user,
        isAuthenticated,
        login,
        logout,
      }),
      [user]
    )

    return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
  };

export function useAuth(){
    const auth = useContext(AuthContext)
    return auth
}

export function Authenticated(props){

    const {user, isAuthenticated, login, logout} = useAuth()

    if ((isAuthenticated===true && user!==null)){
        return (props.children)
    }
    if ((isAuthenticated)===false){
        return (
            <ErrorView message= "Only authenticated users can access this page"/>
        )
    }

    return (<></>)
}

export function NotAuthenticated(props){
    const {user, isAuthenticated, login, logout} = useAuth()

    if (isAuthenticated===false && user===null){
        return (props.children)
    }
    if(isAuthenticated===true){
        return (
            <ErrorView message= "Only unauthenticated users can access this page"/>
        )
    }
    return (<></>)
}
