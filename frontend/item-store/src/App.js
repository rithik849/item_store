import {useState, useEffect} from "react"
import React from "react";
import {LogInView} from "./Authentication/LogInView"
import {LogOutView} from "./Authentication/LogOutView";
import { ChangeDetailsView } from "./Authentication/ChangeDetailsView";
import { ChangePasswordView } from "./Authentication/ChangePasswordView";
import {AuthProvider, Authenticated, NotAuthenticated} from "./components/is_authenticated_component"
import {CookiesProvider} from "react-cookie"
import {createBrowserRouter, createRoutesFromElements, Route, RouterProvider} from 'react-router-dom'
import {ProfileView} from './Authentication/ProfileView'
import { ProductDetailView, Products } from "./Product/product";
import { Baskets } from "./Basket/basket";
import { useAuth } from "./components/is_authenticated_component";
import {url} from "./constants"
import { Orders, OrderDetails } from "./Order/order";


function CreateRoutes(){

  const {isAuthenticated,user,logout,login} = useAuth()

  const router = createBrowserRouter(
    createRoutesFromElements(
        <Route>
            <Route index path="/login" element = {<LogInView/>} />
            <Route path = "/logout" element = {<LogOutView/>} />
            <Route path = "/change-details" element = {<ChangeDetailsView/>} />
            <Route path = "/change-password" element = {<ChangePasswordView/>} />
            <Route path = "/profile" element = {<ProfileView/>}/>
            <Route path = "" element = {<Products/>}/>
            <Route path = "/product/:id" element = {<ProductDetailView/>} />
            <Route path = "/baskets" element = {<Baskets/>}/>
            <Route path = "/orders" element = {<Orders/>} />
            <Route path = "/orders/:date/:id" element = {<OrderDetails/>} />
        </Route>
    )
  )

  return(
    <>
      {isAuthenticated && <p>{user.username}</p>}
      <RouterProvider router={router}/>
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

      fetch(url+"/customers/login/",{
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

  const router = createBrowserRouter(
    createRoutesFromElements(
        <Route>
            <Route index path="/login" element = {<LogInView/>} />
            <Route path = "/logout" element = {<LogOutView/>} />
            <Route path = "/change-details" element = {<ChangeDetailsView/>} />
            <Route path = "/change-password" element = {<ChangePasswordView/>} />
            <Route path = "/profile" element = {<ProfileView/>}/>
            <Route path = "/product" element = {<Products/>}/>
            <Route path = "/product/:id" element = {<ProductDetailView/>} />
        </Route>
    ))

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
    
    //<PaginatedView endpoint="http://localhost:8000/products/?page=1" item={(key,values)=> <Product key={key} values={values}/>} />
  )

};

export default App;
