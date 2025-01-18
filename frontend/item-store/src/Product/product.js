import {url} from "../constants"
import Product from "./product_card"
import {useState, useEffect} from "react"
import { useAuth } from "../components/is_authenticated_component"
import { ReviewForm, Reviews } from "../Review/review_components"
import { useParams} from "react-router-dom"
import PaginatedView from "../components/paginated_component";
import { useNavigate } from "react-router-dom"
import { ErrorView, DisplayMessage } from "../components/errorView"
import { getHeaders, process_errors } from "../utils"

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
    const [message,setMessage] = useState([])
    const [error, setError] = useState(false)

    // Check if product is in the basket, if it is display its quantity instead of 0.
    useEffect(() => {

        const fetchData = async () => {
            let response
            let json

            response = await fetch(url+"/baskets/"+props.id,
                {
                    "method" : "GET",
                    mode : "cors",
                    headers : getHeaders(),
                    credentials : "include"
                }
            )
            json = await response.json()

            if (!response.ok){
                throw Error('Basket item not found')
            }

            setQuantity(json['quantity'])
        }

        fetchData().catch((err) => {
            console.log(err)
        })
    },[props.id])

    async function handleSubmit(event){
        event.preventDefault()
        let response
        let json
        try{
            response = await fetch(url+"/baskets/",
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
            json = await response.json()

            if (!response.ok){
                throw Error('Something went wrong')
            }

            console.log(json)

            if (json['success']){
                setMessage([json['detail']])
                setError(false)
            }else{
                setMessage([json['detail']])
                setError(true)
            }
        }catch (err){
            console.error(err)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(true)
            }
        }
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
        <div className={error ? "text-danger" : "text-success"}>
            <DisplayMessage messages={message}/>
        </div>
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
        const fetchData = async () => {
            let response
            let json

            response = await fetch(url + "/products/"+params.id)
            json = await response.json()

            if (!response.ok){
                throw Error(JSON.stringify(json))
            }

            setData(json)
        }

        fetchData().catch((error) => {
            console.error(error)
            let json = JSON.parse(error.message)
            if ('detail' in json){
                setError(json['detail'])
            }
        })
    },[params.id])

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