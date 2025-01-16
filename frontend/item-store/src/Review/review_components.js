import {useState } from "react"
import {useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import PaginatedView from "../components/paginated_component"
import {getHeaders} from "../utils"

export function ReviewForm(props){

    const {isAuthenticated} = useAuth()

    const [formData,setFormData] = useState({
        "rating" : 1,
        "comment" : ""
    })

    const [message, setMessage] = useState([])

    function submitHandler(event){
        event.preventDefault()
        fetch(url+"/reviews/",
            {
                method : "POST",
                mode : 'cors',
                headers : getHeaders(),
                credentials : "include",
                body : JSON.stringify({
                    "product": props.product,
                    "comment": formData.comment,
                    "rating": formData.rating
                })
            }
        )
        .then((response) => {
            if (!response.ok){
                return Promise.reject(response)
            }

            return response.json()
        })
        .then((json) => {
                alert("Review submitted")
        })
        .catch(async (response) => {
            const json = await response.json()
            console.error(json)
            let errors = ""
            for (let key in json){
                errors += json[key]

            }
            console.error(errors)
            setMessage(errors.split("."))
        })
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
        <div className="w-50 pb-5">
            <h2>{props.values['customer']['username']}, {'★'.repeat(parseInt(props.values['rating']))}</h2>
            <h3>{props.values['comment']}</h3>
        </div>
        )
}

export function Reviews(props){
    return <PaginatedView endpoint={url+"/reviews/"+props.product+"/"} displayClass={"d-flex justify-content-center align-items-center flex-column border border-primary w-100 h-50 overflow-auto"} item={(key,values) => <ReviewCard key={key} values={values}/>}/>
}