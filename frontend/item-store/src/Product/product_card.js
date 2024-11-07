import { useNavigate } from "react-router-dom"
import { url } from "../constants"
import { useState } from "react"

const formatter = new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',})

function Product({key,values}){
    console.log(values)
    const nav = useNavigate()

    function handleClick(event){
        event.preventDefault()
        nav("/product/"+values.id, {state : values})

    }



    return (
    <div key={key} onClick={handleClick}>
        <h2>{values.id}</h2>
        <h2>{"Name: "+values.name} </h2>
        <h2>{"Price: "+formatter.format(values.price)}</h2>
        <h3>{"Stock: "+values.stock}</h3>
        <h3>{"Type: "+values.type}</h3>
    </div>
    )
}

export default Product