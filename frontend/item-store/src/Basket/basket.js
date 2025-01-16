
import { useNavigate } from "react-router-dom"
import { url } from "../constants"
import PaginatedView from "../components/paginated_component";
import { formatter } from "../utils";
import { createContext, useContext } from "react";
import { useCookies } from "react-cookie";
import { useState, useEffect } from "react";
import { Authenticated } from "../components/is_authenticated_component";
// Components to view basket products and change their amounts

const BasketContext = createContext()

export function Baskets(){
    
    const [cookies,setCookies] = useCookies()
    const [msg,setMsg] = useState("")

    async function placeOrder(){
        fetch(url+"/orders/",{
            method : "POST",
            mode : "cors",
            headers : {
                "Content-Type" : 'application/json; charset=UTF-8',
                "Access-Control-Allow-Credentials" : true,
                "X-CSRFToken" : cookies.csrftoken
            },
            credentials : "include"
        })
        .then(response => {
            if (!response.ok){
                return Promise.reject(response)
            }

            return response.json()
        })
        .then(json => {
            setMsg(json)
            alert(json.detail)

        })
        .catch(async (response) => {
            console.error(response)
            try{
                const json = await response.json()
                alert(json['detail'])
            }catch{
                alert('Something went wrong')
            }
        })
    }

    async function handleDel(){
        fetch(url+"/baskets/",{
            method : "DELETE",
            mode : "cors",
            headers : {
                "Content-Type" : 'application/json; charset=UTF-8',
                "Access-Control-Allow-Credentials" : true,
                "X-CSRFToken" : cookies.csrftoken
            },
            credentials : "include"
        })
        .then(response => {
            if (!response.ok){
                return Promise.reject(response)
            }

            return response.json()
        })
        .then(json => {
            setMsg(json)
            alert(json.detail)

        })
        .catch((response) => {
            console.error(response)
            alert('Something went wrong!')
        })
    }

    return <Authenticated>
        <BasketContext.Provider value={[msg,setMsg]}>
            <button onClick={handleDel}>Empty Basket</button>
            <button onClick={placeOrder}>Order</button>
            <PaginatedView endpoint={url+"/baskets/?page=1"} msg={msg} item={(key,values)=> <div key={key}> <Basket key={key} values={values} /> </div> } />
        </BasketContext.Provider>
    </Authenticated>
}

function Basket({key,values}){
    const [cookies] = useCookies()
    const nav = useNavigate()
    const [msg,setMsg] = useContext(BasketContext)
    const [quantity,setQuantity] = useState(0)

    useEffect(() => {
        fetch(url+"/baskets/"+values.product.id,
            {
                "method" : "GET",
                mode : "cors",
                headers : {
                    "Content-Type" : 'application/json; charset=UTF-8',
                    "Access-Control-Allow-Credentials" : true,
                    "X-CSRFToken" : cookies.csrftoken
                },
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

    function generateClickHandler(values){
        const handleClick = (event) => {
            event.preventDefault()
            nav("/product/"+values.product.id, {state : values})

        }
        return handleClick
    }

    function handleRemoveItemFromBasket(){
        fetch(values.url,{
            method : "DELETE",
            mode : "cors",
            headers : {
                "Content-Type" : 'application/json; charset=UTF-8',
                "Access-Control-Allow-Credentials" : true,
                "X-CSRFToken" : cookies.csrftoken
            },
            credentials : "include"
        })
        .then(async res => {
            const json = await res.json()
            alert(json.detail)
            setMsg(json)
        })
        .catch((err) => {
            console.log(err)
            alert(err)
        })
    }

    function changeItemQuantity(event){
        event.preventDefault()
        fetch(values.url,{
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
        .then(async res => {
            const json = await res.json()
            alert(json.detail)
            setMsg(json)
        })
        .catch((err) => {
            console.log(err)
            alert(err)
        })
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
        <h3>{"Type: "+values.product.type}</h3>
    </div>
    <form>
        <input type="number" name="quantity" min={0} max={99} step="1" value={quantity} onChange={handleChange}/>
        <button onClick={changeItemQuantity}>{"Change Item Quantity"}</button>
    </form>
    <button onClick={handleRemoveItemFromBasket}>Remove</button></>
    

}