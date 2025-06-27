import React, { useEffect, useState } from "react";
import { getAlert, postTemperatureAlert } from "../../service/influxService";
import { getAllTemperature as oracleGetAllTemperature, postTemperatureAlert as postTemp } from "../../service/oracleService";
import { TrophySpin } from "react-loading-indicators";
import { Button } from "@mui/material";
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Legend,
  Tooltip,
  Title,
} from "chart.js";
import "./chartCart.css"
ChartJS.register(
  LineElement,
  PointElement,
  LinearScale,
  CategoryScale,
  Legend,
  Tooltip,
  Title
);
const options = {
  responsive: true,
  plugins: {
    legend: { position: "top" },
  },
  scales: {
    x: { title: { 
        display: true,
        text: "Time" },
        grid: {
            display: true
        },
        ticks: {
            maxRotation: 45,  
            minRotation: 90,  
            autoSkip: true,  
        },
        },
    y: { title: { 
        display: true, 
        text: "Temperatur CPU" 
        },
        grid: {
            display: true
        } },
  },
};

function getDataset(temperature){
    console.log("Loaded data")
    const labels = Array.from(new Set(temperature.map(d => d.time))).sort();
    
    const data = temperature.reduce((prev,current) => {
        if(!prev[current.sensor_name])
            prev[current.sensor_name] = {}
        prev[current.sensor_name][current.time] = current.temperature
        return prev
    },{})
    
    const datasets = Object.entries(data).map(([sensor_name, values], idx) => {


    return {
      
      label: sensor_name,
      data: labels.map(label => values[label] ?? null), 
      borderColor: `hsla(${(idx * 60) % 360}, 70%, 60%, 0.8)`,
      backgroundColor: `hsla(${(idx * 60) % 360}, 70%, 70%, 0.3)`,
      fill: false,
      tension: 0.1,
        };
    });
    return { labels, datasets };
}

function Alert({connectionDB}){
    const [inputValue, setInputValue] = useState(0)
    const [alertData,setAlertData] = useState(null)
    const [loading,setLoading] = useState(true)



    const handleChange  = (e) =>{
        setInputValue(e.target.value)
    }
    const sendTemperatureAlert = async () =>{
        connectionDB?  await  postTemp(inputValue) :postTemperatureAlert(inputValue)
    }

    
    useEffect(() =>{
        let isActive = true
        const fetchData = async () =>{
            try{
                const data =  connectionDB? await  oracleGetAllTemperature(): await getAlert();
                if(data){
                    setAlertData(getDataset(data))
                    setLoading(false)
                    }   
                }
                catch(error){
                    console.error("Error: ", error)
                }
        }

        fetchData()

        const intervalId = setInterval(fetchData,10000)
        return () => {
            clearInterval(intervalId)
            isActive = false
        }
    },[connectionDB])

    if (loading || !alertData){
        return(
            <div className="loading">
                <TrophySpin color="#315ccc" size="large" text="loading " textColor="#cba2a2" />
            </div>
        )
    }
    const setAlert = () => {
        return (
            <div class="base-Input-root">
                <input class="base-Input-input" type="number" max={100} min={0} defaultValue={40} onChange={handleChange}/>
                <Button onClick={sendTemperatureAlert()} variant="outlined" sx={{
                    '&:hover': {
                    backgroundColor: '#282c34',
                    color:"#F5DEB3"
                    },
                }}>Send</Button>
            </div>
        )
    }
    
    <ul>
        <li>Show alert</li>
        <li>Set Alert</li>
    </ul>
} 