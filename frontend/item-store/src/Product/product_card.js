import { formatter } from "../utils"

function Product({values}){


    return (
    <div>
        <h2>{values.id}</h2>
        <h2>{"Name: "+values.name} </h2>
        <h2>{"Price: "+formatter.format(values.price)}</h2>
        <h3>{"Stock: "+values.stock}</h3>
    </div>
    )
}

export default Product