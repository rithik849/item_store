import { useNavigate } from "react-router-dom"
import { url } from "../constants"
import PaginatedView from "../components/paginated_component";
import { formatter } from "../utils";
import { createContext, useContext } from "react";
import { useCookies } from "react-cookie";
import { useState } from "react";
// Components to view basket products and change their amounts

const BasketContext = createContext()

export function Baskets(){
    
    const [cookies,setCookies] = useCookies()
    const [msg,setMsg] = useState("")

    


    async function handleDel(){
        const response = fetch(url+"/baskets/",{
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
            setMsg(json)
            alert(json.detail)

        })
        .catch((err) => {
            console.log(err)
            alert('Something went wrong!')
        })
    }
    return <BasketContext.Provider value={[msg,setMsg]}>
    <button onClick={handleDel}>Empty Basket</button>
    <PaginatedView endpoint={url+"/baskets/?page=1"} msg={msg} item={(key,values)=> <div key={key}> <Basket key={key} values={values} /> </div> } />
    </BasketContext.Provider>
}

function Basket({key,values}){
    console.log(values)
    const [cookies,setCookies] = useCookies()
    const nav = useNavigate()
    const [msg,setMsg] = useContext(BasketContext)

    function generateClickHandler(values){
        const handleClick = (event) => {
            event.preventDefault()
            nav("/product/"+values.product.id, {state : values})

        }
        return handleClick
    }

    function handleRemoveItemFromBasket(){
        const response = fetch(values.url,{
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
            alert('Something went wrong!')
        })
    }


    return <>
    <div key={key} onClick={generateClickHandler(values)}>
        <h2>{"Name: "+values.product.name} </h2>
        <h2>{"Price: "+formatter.format(values.product.price)}</h2>
        <h3>{"Quantity: "+values.quantity}</h3>
        <h3>{"Type: "+values.product.type}</h3>
    </div>
    <button onClick={handleRemoveItemFromBasket}>Remove</button></>
}