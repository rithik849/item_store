import {useState } from "react"
import { useCookies } from "react-cookie"
import { useAuth } from "../components/is_authenticated_component"
import {url} from "../constants"
import PaginatedView from "../components/paginated_component"

export function ReviewForm(props){

    const {user, isAuthenticated, login, logout} = useAuth()

    const [formData,setFormData] = useState({
        "rating" : 1,
        "comment" : ""
    })

    const [cookies,setCookies] = useCookies()

    const [message, setMessage] = useState([])

    function submitHandler(event){
        event.preventDefault()
        fetch(url+"/reviews/",
            {
                method : "POST",
                mode : 'cors',
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include",
                body : JSON.stringify({
                    "product": props.product,
                    "comment": formData.comment,
                    "rating": formData.rating
                })
            }
        ).then(
            async (response) => {
                if (response.status===200){
                    alert("Review submitted")
                }else{
                    const json = await response.json()
                    console.log(json)
                    let errors = ""
                    for (let key in json){
                        errors += json[key]

                    }
                    console.log(errors)
                    setMessage(errors.split("."))
                }
            }
        )
    }

    const handleChange = (event) => {
        event.preventDefault()
        setFormData(values => ({...formData,[event.target.name] : event.target.value}))


    }

    return (
        isAuthenticated && 
        <>
        <form onSubmit={submitHandler}>
            <label>Rating</label>
            <input type="number" name="rating" min="1" max="5" onChange={handleChange}></input>
            <label>Review</label>
            <input type="text" name="comment" onChange={handleChange}></input>
            <button type="submit" >Create Review</button>
        </form>
        {
            message.map(
                (error,index) => <p key={index}>{error}</p>
            )
        }
        </>
    )

}

function ReviewCard(props){
    console.log(props)
    return (
        <div>
            <h2>{props.values['customer']['username']}, {'★'.repeat(parseInt(props.values['rating']))}</h2>
            <h3>{props.values['comment']}</h3>
        </div>
        )
}

export function Reviews(props){
    return <PaginatedView endpoint={url+"/reviews/"+props.product+"/"} item={(key,values) => <ReviewCard key={key} values={values}/>}/>
}