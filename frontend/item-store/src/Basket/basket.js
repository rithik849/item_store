
import { useNavigate } from "react-router-dom"
import { url } from "../constants"
import PaginatedView from "../components/paginated_component";
import { formatter, getHeaders, process_errors } from "../utils";
import { createContext, useContext } from "react";
import { useCookies } from "react-cookie";
import { useState, useEffect } from "react";
import { Authenticated } from "../components/is_authenticated_component";
import { DisplayMessage } from "../components/errorView";

// Components to view basket products and change their amounts

const BasketContext = createContext()

export function Baskets(){
    
    const [cookies,setCookies] = useCookies()
    const [message,setMessage] = useState([])
    const [isError,setError] = useState(false)

    async function placeOrder(){
        let response
        let json
        try{
            response = await fetch(url+"/orders/",{
                method : "POST",
                mode : "cors",
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include"
            })
            json = await response.json()
            if (!response.ok){
                throw Error('Something went wrong')
            }
            setMessage(json.detail)
            setError(false)
            alert(json.detail)

        }catch (error){
            console.error(error)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(false)
                alert(error_messages)
            }
        }

    }

    async function handleDel(){
        let response
        let json
        try{
            response = await fetch(url+"/baskets/",{
                method : "DELETE",
                mode : "cors",
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include"
            })
            json = await response.json()
            setMessage([json.detail])
            setError(true)

        }catch (error){
            console.error(error)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(false)
                alert(error_messages)
            }
        }
    }

    return <Authenticated>
        <BasketContext.Provider value={[setMessage,setError]}>
            <button onClick={handleDel}>Empty Basket</button>
            <button onClick={placeOrder}>Order</button>
            <div className = {isError ? 'text-danger' : 'text-success'}>
            <DisplayMessage messages={message}/>
            </div>
            <PaginatedView endpoint={url+"/baskets/?page=1"} msg={message} item={(key,values)=> <div key={key}> <Basket key={key} values={values} /> </div> } />
        </BasketContext.Provider>
    </Authenticated>
}

function Basket({key,values}){
    const [cookies] = useCookies()
    const nav = useNavigate()
    const [setMessage,setError] = useContext(BasketContext)
    const [quantity,setQuantity] = useState(0)

    useEffect(() => {
        const fetchData = async () => {
            let response
            let json

            response = await fetch(url+"/baskets/"+values.product.id,
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
    },[])

    function generateClickHandler(values){
        const handleClick = (event) => {
            event.preventDefault()
            nav("/product/"+values.product.id, {state : values})

        }
        return handleClick
    }

    async function handleRemoveItemFromBasket(event){
        event.preventDefault()
        let response
        let json
        try{
            response = await fetch(values.url,{
                method : "DELETE",
                mode : "cors",
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include"
            })
            json = await response.json()

            if (!response.ok){
                throw Error('Something went wrong')
            }

            alert(json.detail)
            setMessage([json.detail])
            setError(true)
        }catch (error){
            console.error(error)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(true)
            }
        }
    }

    async function changeItemQuantity(event){
        event.preventDefault()
        let response
        let json
        try{
            response = await fetch(values.url,{
                method : "PATCH",
                mode : "cors",
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
                credentials : "include",
                body:JSON.stringify({
                    "quantity" : quantity
                })
            })

            json = await response.json()
            alert(json.detail)
            setMessage([json.detail])
            setError(false)


        }catch (error){
            console.error(error)
            if (json){
                let error_messages = process_errors(json)
                setMessage(error_messages)
                setError(true)
            }
            alert(error)
        }
    }

    function handleChange(event){
        event.preventDefault()
        setQuantity((prev) => parseInt(event.target.value))
    }


    return <>
    <div key={key} onClick={generateClickHandler(values)}>
        <h2>{"Name: "+values.product.name} </h2>
        <h2>{"Price: "+formatter.format(values.product.price)}</h2>
        <h3>{"Quantity: "+values.quantity}</h3>
    </div>
    <form>
        <input type="number" name="quantity" min={0} max={99} step="1" value={quantity} onChange={handleChange}/>
        <button onClick={changeItemQuantity}>{"Change Item Quantity"}</button>
    </form>
    <button onClick={handleRemoveItemFromBasket}>Remove</button></>
    

}