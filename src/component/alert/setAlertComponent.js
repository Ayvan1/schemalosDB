import React,{useEffect,useState} from "react";
import { getAlert, postTemperatureAlert } from "../../service/influxService";
import { postTemperatureAlert as postTemp } from "../../service/oracleService";
import { Button } from "@mui/material";




function SetAlertComponent({connectionDB}){
    const [inputValue,setInputValue] = useState(40)
    
    const handleChange = (e) =>{
        setInputValue(e.target.value)
    }

    const sendTemperatureAlert = async () =>{
        connectionDB? await postTemp(inputValue):postTemperatureAlert(inputValue)
    }

    return(
        <>
            <div class="base-Input-root">
                <input class="base-Input-input" type="number" max={100} min={0} defaultValue={40} onChange={handleChange}/>
            </div>
            <Button onClick={sendTemperatureAlert()} variant="outlined" sx={{
                    '&:hover': {
                    backgroundColor: '#282c34',
                    color:"#F5DEB3"
                    },
            }}>Send</Button>
        </>
    )
}