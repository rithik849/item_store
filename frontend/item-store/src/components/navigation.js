import { NavLink } from "react-router-dom";
import { useAuth } from "./is_authenticated_component";
import { Outlet } from "react-router-dom";


export function Navigation(props){

    const {isAuthenticated,user,logout,login} = useAuth()

    return (
        <div>
            <nav>
                <NavLink to={""}>{'Home'}</NavLink>
                {isAuthenticated && 
                <>
                <NavLink to='/profile'>Profile</NavLink>
                <NavLink to='/orders'>Orders</NavLink>
                <NavLink to='/baskets'>Basket</NavLink>
                <NavLink to='/logout'>Log Out</NavLink>
                </>
                }
                {!isAuthenticated &&
                <>
                <NavLink to='/login'>Log In</NavLink>
                </>
                }
            </nav>
            {isAuthenticated && <p>{user.username}</p>}
            {<Outlet/>}
        </div>

    )
}