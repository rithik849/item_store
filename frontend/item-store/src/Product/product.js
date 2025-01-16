import {url} from "../constants"
import Product from "./product_card"
import {useState, useEffect} from "react"
import { useAuth } from "../components/is_authenticated_component"
import { ReviewForm, Reviews } from "../Review/review_components"
import { useParams} from "react-router-dom"
import PaginatedView from "../components/paginated_component";
import { useNavigate } from "react-router-dom"
import { ErrorView } from "../components/errorView"
import { getHeaders } from "../utils"

export function Products(){
    const nav = useNavigate()
    
    function generateClickHandler(values){
        const handleClick = (event) => {
            event.preventDefault()
            nav("/product/"+values.id, {state : values})

        }
        return handleClick
    }
    return <PaginatedView endpoint={url+"/products/?page=1"} msg={""} displayClass="d-flex flex-row flex-wrap justify-content-center" item={(key,values)=> <div key={key} className="border border-danger rounded px-2" onClick={generateClickHandler(values)}> <Product values={values} /> </div> } />
}


export function AddProductToBasketForm(props){

    const [quantity, setQuantity] = useState(0)
    const [message,setMessage] = useState("")
    const [error, setError] = useState(false)

    // Check if product is in the basket, if it is display its quantity instead of 0.
    useEffect(() => {
        fetch(url+"/baskets/"+props.id,
            {
                "method" : "GET",
                mode : "cors",
                headers : getHeaders(),
                credentials : "include"
            }
        )
        .then(response => {
            if (!response.ok){
                return Promise.reject(response)
            }
            return response.json()
        })
        .then(json => {
            console.log(json['quantity'])
            setQuantity(json['quantity'])
        })
        .catch(response => {
            console.error(response)
        })
    },[])

    function handleSubmit(event){
        event.preventDefault()
        fetch(url+"/baskets/",
            {
                method : "POST",
                mode : 'cors',
                headers : getHeaders(),
                credentials : "include",
                body : JSON.stringify({
                    "product" : props.id,
                    "quantity" : quantity
                })
            }
        )
        .then(response => {
            if (response.ok){
                return response.json()
            }
            return Promise.reject(response)
        }).then(json => {
            if (json['success']){
                setMessage(json['detail'])
                setError(false)
            }
            else{
                setMessage(json['detail'])
                setError(true)
            }
        }).catch(async response => {
            if ('json' in response){
                let json = await response.json()
                setMessage(json['detail'])
                setError(true)
            }
            console.error(response)

        })
    }

    function handleChange(event){
        event.preventDefault()
        setQuantity((prev) => parseInt(event.target.value))
    }

    return (
        <>
        <form>
            <input type="number" name="quantity" min={0} max={99} step="1" value={quantity} onChange={handleChange}/>
            <button onClick={handleSubmit}>{"Add to Basket"}</button>
        </form>
        <p className={error ? "text-danger" : "text-success"}>{message}</p>
        </>
    )
}

export function ProductDetailView(){
    /*
    Have product details
    Form to add and remove stock from basket if authenticated
    View reviews for the product
    Form to add review for the product if authenticated
    */

    const params = useParams()
    const [data, setData] = useState(null)
    const [error,setError] = useState(null)
    const {isAuthenticated} = useAuth()

    useEffect(() => {
        fetch(url + "/products/"+params.id)
        .then(response => {

            if (!response.ok){
                return Promise.reject(response)
            }
            return response.json()
        })
        .then(json =>{
            setData(json)
        })
        .catch(async (response) => {
            const json = await response.json()
            console.error(response)
            if (json['detail']!==undefined){
                setError(json['detail'])
            }
        })
    },[])

    if (error!==null){
        return <ErrorView message = {error} />
    }

    return (
        data!==null && 
        <>
            <Product key={1} values={data} />
            {isAuthenticated && <AddProductToBasketForm id={params.id} />}
            {isAuthenticated && <ReviewForm product={params.id} />}
            <Reviews product={params.id}/>
        </>
    )






}