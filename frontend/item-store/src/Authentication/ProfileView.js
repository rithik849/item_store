import { useAuth, Authenticated } from "../components/is_authenticated_component"
import { NavLink } from "react-router-dom";

export function ProfileView(){

    const {user, isAuthenticated} = useAuth()


    return ( 
        <Authenticated>
            {isAuthenticated && 
                <>
                    <NavLink className="btn btn-outline-secondary text-black" to='/change-details'>Change Details</NavLink>
                    <NavLink className="btn btn-outline-secondary text-black" to='/change-password'>Change Password</NavLink>
                    <div className="d-flex flex-column align-items-center">
                        <div className="d-flex flex-column rounded align-items-center justify-content-center border border-gray">
                            <h3>{user.username}</h3>
                            <h3>{user.email}</h3>
                            
                        </div>
                    </div>
                </>
            }
        </Authenticated>
    )
}