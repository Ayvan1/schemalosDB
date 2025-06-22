import React, { useEffect, useState } from "react";
import { getAllTemperature } from "../../service/influxService";
import { getAllTemperature as oracleGetAllTemperature } from "../../service/oracleService";

function Alert({connectionDB}){
    const [inputValue, setInputValue] = useState(0)
    const [alertData,setAlertData] = useState(null)
    const [loading,setLoading] = useState(true)
    const handleChange  = (e) =>{
        setInputValue(e.target.value)
    }
    useEffect(() =>{
        const fetchData = async () =>{
            try{
            const data =  connectionDB? await  oracleGetAllTemperature(): await getAllTemperature();
            if(data){
                 setAlertData(data)
                 setLoading(false)
                }   
            }
            catch(error){
                console.error("Error: ", error)
            }
        }

        fetchData()
        if(inputValue){
            const intervalId = setInterval(fetchData,10000)
            
        }
        
    },[connectionDB])
    const setAlert = () => {
        return (
            <>
                <input type="number" max={100} min={0} defaultValue={0} onChange={handleChange}></input>
            </>
        )
    }
    
    <ul>
        <li>Show alert</li>
        <li>Set Alert</li>
    </ul>
}