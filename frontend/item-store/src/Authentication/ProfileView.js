import { useAuth, Authenticated } from "../components/is_authenticated_component"
import { NavLink } from "react-router-dom";

export function ProfileView(){

    const {user, isAuthenticated} = useAuth()


    return ( 
        <Authenticated>
            {isAuthenticated && 
                <>
                    <NavLink to='/change-details'>Change Details</NavLink>
                    <NavLink to='/change-password'>Change Password</NavLink>
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