import React,{useEffect,useState} from "react";
import { postTemperatureAlert } from "../../service/influxService";
import { postTemperatureAlert as postTemp } from "../../service/oracleService";
import { Button,TextField } from "@mui/material";
import "./alert.css"



function SetAlertComponent({connectionDB}){
    const [inputValue,setInputValue] = useState(40)
    
    const handleChange = (e) =>{
        setInputValue(e.target.value)
    }

    const sendTemperatureAlert = async () =>{
        connectionDB? await postTemp(inputValue): await postTemperatureAlert(inputValue)
    }

    return(
        <div className="sendAlert">
            <div className="TempInput">
                <TextField
                    label="Enter a number"
                    type="number"
                    variant="outlined"
                    defaultValue={40}
                    onChange={handleChange}
                    InputLabelProps={{
                        shrink: true,
                    }}
                    inputProps={{
                        min: 0,
                        max: 100,
                        step: 1,
                    }}
                    />
            </div>

            <div>
                <Button onClick={sendTemperatureAlert} variant="outlined" sx={{
                        '&:hover': {
                        backgroundColor: '#282c34',
                        color:"#F5DEB3"
                        },
                    }}>Send</Button>
            </div>  
            
                
                
                
                {/* <input class="base-Input-input" type="number" max={100} min={0} defaultValue={40} onChange={handleChange}/> */}
            
            
        </div>
    )
}


export default SetAlertComponent