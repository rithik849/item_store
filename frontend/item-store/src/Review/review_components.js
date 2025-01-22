import {useState} from "react"
import {useAuth} from "../components/is_authenticated_component"
import {url} from "../constants"
import PaginatedView from "../components/paginated_component"
import {getHeaders, process_errors} from "../utils"
import { DisplayMessage } from "../components/errorView"

export function ReviewForm(props){

    const {isAuthenticated} = useAuth()

    const [formData,setFormData] = useState({
        "rating" : 1,
        "comment" : ""
    })

    const [message, setMessage] = useState([])
    const [isError, setError ] = useState(false)

    async function submitHandler(event){
        event.preventDefault()
        const controller = new AbortController();
        const abort_signal = controller.signal
        let response
        let json

        try{
            response = await fetch(url+"/reviews/",
                {
                    method : "POST",
                    mode : 'cors',
                    headers : getHeaders(),
                    credentials : "include",
                    signal : abort_signal,
                    body : JSON.stringify({
                        "product": props.product,
                        "comment": formData.comment,
                        "rating": formData.rating
                    })
                }
            )
            json = await response.json()

            if (!response.ok){
                throw Error(JSON.stringify(json))
            }
            alert('Review Submitted')
            props.submitted(true)
        }catch (error){
            console.error(error)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(true)
            }
        }
        return () => {controller.abort()}
    }

    const handleChange = (event) => {
        event.preventDefault()
        setFormData(values => ({...formData,[event.target.name] : event.target.value}))


    }

    return (
        isAuthenticated && 
        <>
        <form onSubmit={submitHandler}>
            <div className="d-flex flex-column align-items-start bg-info ps-3 input group input-group-lg">
                <label className="fw-bold">Rating</label>
                <input type="number" name="rating" min="1" max="5" onChange={handleChange}></input>
                <label className="fw-bold">Review</label>
                <input className="input-group-text" type="text" name="comment" onChange={handleChange}></input>
                <button type="submit" className="btn border border-info my-2 bg-primary">Create Review</button>
            </div>
        </form>
        <div className={isError ? 'text-danger' : 'text-success'}>
            <DisplayMessage messages={message}/>
        </div>
        </>
    )

}

function ReviewCard(props){
    console.log(props)
    return (
        <div className="w-50 pb-5 border rounded">
            <h2>{props.values['customer']['username']}, {'★'.repeat(parseInt(props.values['rating']))}</h2>
            <h3>{props.values['comment']}</h3>
        </div>
        )
}

export function Reviews(props){

    return <PaginatedView rerender={props.rerender} endpoint={url+"/reviews/"+props.product+"/"} displayClass={"d-flex justify-content-center align-items-center flex-column border-top border-primary h-50 overflow-scroll"} item={(key,values) => <ReviewCard key={key} values={values}/>}/>
}

export function ReviewsComponent({product}){
    const [rerender, setRerender] = useState(false)
    const {isAuthenticated} = useAuth()

    return (
        <>
            {isAuthenticated && <ReviewForm product={product} submitted={setRerender}/>}
            <Reviews rerender={rerender} product={product}/>
        </>
    )
}