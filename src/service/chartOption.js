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
export const options = {
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

export function getDataset(temperature){
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

