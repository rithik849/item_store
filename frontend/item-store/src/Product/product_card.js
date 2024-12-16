import { useNavigate } from "react-router-dom"
import { url } from "../constants"
import { useState } from "react"
import { formatter } from "../utils"

function Product({key,values}){
    console.log(values)


    return (
    <div key={key}>
        <h2>{values.id}</h2>
        <h2>{"Name: "+values.name} </h2>
        <h2>{"Price: "+formatter.format(values.price)}</h2>
        <h3>{"Stock: "+values.stock}</h3>
        <h3>{"Type: "+values.type}</h3>
    </div>
    )
}

export default Product