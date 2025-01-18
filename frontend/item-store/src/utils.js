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

export function process_errors(json){
    let error_messages = []
    for (let key in json){
        console.log(key)
        if (Array.isArray(json[key])){
            error_messages = error_messages.concat(json[key])
        }else{
            error_messages.push(json[key])
        }
    }
    console.log(error_messages)
    return error_messages
}