import { NavLink } from "react-router-dom";
import { useAuth } from "./is_authenticated_component";
import { Outlet } from "react-router-dom";
import { useEffect, useState } from "react";

export function Navigation(){

    const {isAuthenticated,user} = useAuth()
    const [username,setUsername] = useState("")

    useEffect(()=>{
        if (user!==""){
            setUsername(user.username)
        }else{
            setUsername("")
        }
    },[user.username,user.email])

    return (
        <div>
            <div className='d-flex justify-content-center py-3 w-100 bg-light mb-2'>
                {isAuthenticated ? <p className="position-absolute start-0 text-info bg-secondary rounded px-2 h-2 justify-self-left">{username}</p> : ""}
                <nav className="navbar nav-pills">
                    <NavLink className='nav-item navbar-item' to={"/"}>{'Home'}</NavLink>
                    {isAuthenticated ? 
                    <>
                    <NavLink className='nav-item navbar-item' to='/profile'>Profile</NavLink>
                    <NavLink className='nav-item navbar-item' to='/orders'>Orders</NavLink>
                    <NavLink className='nav-item navbar-item' to='/baskets'>Basket</NavLink>
                    <NavLink className='nav-item navbar-item' to='/logout'>Log Out</NavLink>
                    </> :
                    ""
                    }
                    {!isAuthenticated ?
                    <>
                    <NavLink className='nav-item navbar-item' to='/login'>Log In</NavLink>
                    <NavLink className='nav-item navbar-item' to='/signup'>Sign Up</NavLink>
                    </> :
                    ""
                    }
                </nav>
            </div>
            <div>
                {<Outlet/>}
            </div>
        </div>

    )
}