import {useNavigate, useParams } from "react-router-dom"
import PaginatedView from "../components/paginated_component"
import { formatter } from "../utils"
import { url } from "../constants"
import { Authenticated } from "../components/is_authenticated_component"

export function Order({key,values}){
    return (
        <div className='item'>
            <h2>{values.id}</h2>
            <h2>{"Date: "+values.date} </h2>
            <h2>{"Total : "+formatter.format(values.total_cost)}</h2>
        </div>
        )
}

export function OrderItem({values}){
    return (
        <div className='item'>
            <h2>Product Name: {values.product.name}</h2>
            <h2>Price: {formatter.format(values.product.price)}</h2>
            <h2>Quantity: {values.quantity}</h2>
        </div>
    )
}

export function OrderDetails(){

    const params = useParams()

    return <Authenticated><PaginatedView endpoint={url+"/orders/"+params.date+"/"+params.id+"/"} msg={""} displayClass="d-flex flex-row flex-wrap justify-content-center" item={(key,values)=> <div key={key} className="border border-danger rounded px-2" > <OrderItem values={values} /> </div>}/></Authenticated>
}

export function Orders(){
    const nav = useNavigate()
    
    function generateClickHandler(values){
        const handleClick = (event) => {
            event.preventDefault()
            nav("/orders/"+values.date+"/"+values.id, {state : values})
        }
        return handleClick
    }
    return <Authenticated><PaginatedView endpoint={url+"/orders/?page=1"} msg={""} displayClass="d-flex flex-row flex-wrap justify-content-center" item={(key,values)=> <div key={key} onClick={generateClickHandler(values)} className="border border-danger rounded px-2"> <Order values={values} /> </div> } /></Authenticated>

}