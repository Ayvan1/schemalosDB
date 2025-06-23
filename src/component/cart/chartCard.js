import React, { useEffect, useState } from "react";
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

import { getAllTemperature } from "../../service/influxService";
import { getAllTemperature as oracleGetAllTemperature } from "../../service/oracleService";
import { TrophySpin } from "react-loading-indicators";
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

function ChartCard({connectionDB}) {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isActive = true;

    const fetchData = async () => {
      try {
        console.log(connectionDB)
        const data =  connectionDB? await  oracleGetAllTemperature(): await getAllTemperature();
        if (isActive && data) {
          setChartData(getDataset(data));
          setLoading(false);
        }
      } catch (error) {
        console.error("Error: ", error);
      }
    };

    fetchData();
    const intervalId = setInterval(fetchData, 10000);

    return () => {
      clearInterval(intervalId);
      isActive = false;
    };
  }, [connectionDB]);

  if (loading || !chartData) {
    return ( <div className="loading" >
                <TrophySpin color="#315ccc" size="large" text="loading " textColor="#cba2a2" />
            </div>
    )
   
  }

  return (
    <div className="cart">
      <h1 >Temperatur Sensor</h1>
      <div className="cart_item">
        <Line data={chartData} options={options} />
      </div>
    </div>
  );
}

export default ChartCard