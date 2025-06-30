const url = "http://10.20.110.65:8081/:8081"


export async function getAllTemperature() {
    const response =  await fetch(`${url}/all_temperature`)
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async function getTemperatureByTime(time) {
    const response =  await fetch(`${url}/temperature_time/${time}`)
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async function getTemperatureBySensor(sensor_name) {
    const response =  await fetch(`${url}/temperature_sensor/${sensor_name}`)
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async  function getAlert(){
    const response = await fetch(`${url}/get_alert`)
    if(!response.ok){
        return null
    }
    return await response.json()
}

export async function postTemperatureAlert(alertTemperature){
    await fetch(`${url}/set_alert/`,{
        method: 'POST',
        headers:{
            "Content-Type":"application/json"
        },
        body: JSON.stringify({
            temperature: alertTemperature
        })
    }).then(res => res.json())
    .then(data => {
        console.log(`--- response ${data}} ---`)
    })
    .catch(error => {
        console.error(`---- error ${error} ---`)
    })
}