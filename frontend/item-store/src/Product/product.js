import {url} from "../constants"
import Product from "./product_card"
import {useState, useEffect} from "react"
import { useAuth } from "../components/is_authenticated_component"
import { useCookies } from "react-cookie"
import { ReviewForm, Reviews } from "../Review/review_components"
import { useParams , useLocation } from "react-router-dom"
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
    return <PaginatedView endpoint={url+"/products/?page=1"} msg={""} item={(key,values)=> <div key={key} onClick={generateClickHandler(values)}> <Product key={key} values={values} /> </div> } />
}


export function AddProductToBasketForm(props){

    const [quantity, setQuantity] = useState(0)
    const [message,setMessage] = useState("")

    const [cookies,setCookies] = useCookies()

    // Check if product is in the basket, if it is display its quantity instead of 0.
    useEffect(() => {
        fetch(url+"/baskets/"+props.id,
            {
                "method" : "GET",
                mode : "cors",
                headers : getHeaders(),
                credentials : "include"
            }
        ).then(async (response) => {
            const json = await response.json()
            if (response.status===200){
                console.log(json['quantity'])
                setQuantity(json['quantity'])
            }
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
        ).then(async (response) => {
            const json = await response.json()
            console.log(json)
            if (response.status===200){
                setMessage(json['detail'])
            }
            else{
                setMessage(JSON.stringify(json))
            }
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
        <p>{message}</p>
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
    const location = useLocation()
    const [data, setData] = useState(null)
    const [error,setError] = useState(null)
    const {isAuthenticated, user, login, logout} = useAuth()

    useEffect(() => {
        fetch(url + "/products/"+params.id).then(async response =>{
            const json = await response.json()
            if (response.status===200){
                setData(json)
            }
            else{
                setError(json)
            }
        })
    },[])

    if (error!==null){
        return <ErrorView message = {error['detail']} />
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