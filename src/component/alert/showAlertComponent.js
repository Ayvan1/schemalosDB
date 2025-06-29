import React, {useEffect,useState} from "react";
import { getAlert as getAlertInflux } from "../../service/influxService";
import { getAlert as getAlertOracle } from "../../service/oracleService";
import { getDataset,options } from "../../service/chartOption";
import { Line } from 'react-chartjs-2';
import "../cart/chartCart.css"
import { TrophySpin } from "react-loading-indicators";

function ShowAlertComponent({connectionDB}){
    const [alertData,setAlertData] = useState(null)
    const [loading,setLoading] = useState(true)

    useEffect(() => {
        let isActive = true
        const fetchData = async () => {
            try {
                const data = connectionDB? await getAlertOracle(): await  getAlertInflux()
                if(data){
                    setAlertData(getDataset(data))
                    setLoading(false)
                }
            }
            catch(error){
                console.error(`--- error: ${error}`)
            }
        }

        fetchData()

        const intervalID = setInterval(fetchData,10000)

        return  () => {
            clearInterval(intervalID)
            isActive = false
        }
    },[connectionDB])

    if(loading || !alertData){
        return(
            <div className="loading">
                <TrophySpin color="#315ccc" size="large" text="loading " textColor="#cba2a2" />
            </div>
        )
    }

    return (
        <div className="cart">
              <h1 >Alert</h1>
              <div className="cart_item">
                <Line data={alertData} options={options} />
              </div>
        </div>
    )
}

export default ShowAlertComponent