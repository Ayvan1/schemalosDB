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

import { getAllTemperature } from "../../service/oracleService";
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
    title: {
      display: true,
      text: "Températures par capteur",
    },
  },
  scales: {
    x: { title: { display: true, text: "Temps" } },
    y: { title: { display: true, text: "Température (°C)" } },
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
      borderColor: `hsl(${(idx * 60) % 360}, 70%, 50%)`,
      fill: false,
      tension: 0.3,
        };
    });
    return { labels, datasets };
}

function ChartCard() {
  const [chartData, setChartData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let isActive = true;

    const fetchData = async () => {
      try {
        const data = await getAllTemperature();
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
  }, []);

  if (loading || !chartData) {
    return <p>Chargement des données...</p>;
  }

  return (
    <>
      <h1>Hi</h1>
      <Line data={chartData} options={options} />
    </>
  );
}

export default ChartCard