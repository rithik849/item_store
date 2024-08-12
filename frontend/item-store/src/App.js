import {useState, useEffect} from "react"
import React from "react";
import PaginatedView from "./components/paginated_component";
import Product from "./components/product_card";
import {LogInView} from "./Authentication/LogInView"
import {LogOutView} from "./Authentication/LogOutView";
import { ChangeDetailsView } from "./Authentication/ChangeDetailsView";
import { ChangePasswordView } from "./Authentication/ChangePasswordView";
import {AuthProvider, Authenticated, NotAuthenticated} from "./components/is_authenticated_component"
import {CookiesProvider} from "react-cookie"
import {createBrowserRouter, createRoutesFromElements, Route, RouterProvider} from 'react-router-dom'
import {ProfileView} from './Authentication/ProfileView'


function App() {

  const [state, setState]= useState(null);

  const router = createBrowserRouter(
    createRoutesFromElements(
        <Route>
            <Route index path="/login" element = {<LogInView/>} />
            <Route path = "/logout" element = {<LogOutView/>} />
            <Route path = "/change-details" element = {<ChangeDetailsView/>} />
            <Route path = "/change-password" element = {<ChangePasswordView/>} />
            <Route path = "/profile" element = {<ProfileView/>}/>
        </Route>
))

  return (
    <React.StrictMode>
      <AuthProvider>
        <CookiesProvider>
          <RouterProvider router={router}/>
        </CookiesProvider>
      </AuthProvider>
    </React.StrictMode>
    
    //<PaginatedView endpoint="http://localhost:8000/products/?page=1" item={(key,values)=> <Product key={key} values={values}/>} />
  )

};

export default App;
