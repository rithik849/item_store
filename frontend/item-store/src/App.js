import {useState, useEffect} from "react"
import React from "react";
import {LogInView} from "./Authentication/LogInView"
import {LogOutView} from "./Authentication/LogOutView";
import { ChangeDetailsView } from "./Authentication/ChangeDetailsView";
import { ChangePasswordView } from "./Authentication/ChangePasswordView";
import {AuthProvider} from "./components/is_authenticated_component"
import {CookiesProvider} from "react-cookie"
import {createBrowserRouter, createRoutesFromElements, Route, RouterProvider} from 'react-router-dom'
import {ProfileView} from './Authentication/ProfileView'
import { ProductDetailView, Products } from "./Product/product";
import { Baskets } from "./Basket/basket";
import {url} from "./constants"
import { Orders, OrderDetails } from "./Order/order";
import { Navigation } from "./components/navigation";
import 'bootstrap/dist/css/bootstrap.min.css';
import { SignUpView } from "./Authentication/SignUpView";


function CreateRoutes(){


  const router = createBrowserRouter(
    createRoutesFromElements(
        <Route element={<Navigation/>}>
            <Route index path = "" element = {<Products/>}/>
            <Route path = "/product/:id" element = {<ProductDetailView/>} />
            <Route path="/login" element = {<LogInView/>} />
            <Route path = "/logout" element = {<LogOutView/>} />
            <Route path = "/signup" element = {<SignUpView/>} />
            <Route path = "/change-details" element = {<ChangeDetailsView/>} />
            <Route path = "/change-password" element = {<ChangePasswordView/>} />
            <Route path = "/profile" element = {<ProfileView/>}/>
            <Route path = "/baskets" element = {<Baskets/>}/>
            <Route path = "/orders" element = {<Orders/>} />
            <Route path = "/orders/:date/:id" element = {<OrderDetails/>} />
        </Route>
    )
  )

  return(
    <>
      <RouterProvider router={router}>
        <Navigation/>
      </RouterProvider>
    </>
  )
}

function App() {

    const [user,setUser] = useState(null)
    const [isAuthenticated, setAuthenticated] = useState(null)

    useEffect(() => {
        console.log("EFFECT MAIN")
        const controller = new AbortController();
        const abort_signal = controller.signal

        const fetchData = async () => {
            let response
            let json

            response = await fetch(url+"/customers/login/",{
                method:"GET",
                credentials:"include",
                signal:abort_signal
                }
            )
            json = await response.json()

            if (!response.ok){
                throw Error('Something went wrong')
            }

            if (json.is_authenticated){
                setUser(json.customer)
                setAuthenticated(json.is_authenticated)
            }else{
                setUser({'username':"",'email':""})
                setAuthenticated(false)
            }
        }

        fetchData().catch(error => {
            console.log(error)
            if (!controller.signal.aborted){
                console.log("Signal not aborted")
            }
        })

        return () => {controller.abort()}
    },[])

    return (
        <React.StrictMode>
        {
            isAuthenticated!==null && 
            <AuthProvider user={user} isAuthenticated={isAuthenticated}>
            <CookiesProvider>
                <CreateRoutes/>
            </CookiesProvider>
            </AuthProvider>
        }
        </React.StrictMode>
        
    )

};

export default App;
