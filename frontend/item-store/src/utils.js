import {Cookies} from "react-cookie"

export const formatter = new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'GBP',})

export function getHeaders(){
    const cookie = new Cookies()
    const header = {
        "Content-Type" : 'application/json; charset=UTF-8',
        "Access-Control-Allow-Credentials" : true,
    }

    const csrftoken = cookie.get('csrftoken')
    if (csrftoken){
        header['X-CSRFToken'] = csrftoken
    }
    return header
}