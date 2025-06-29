const url = "http://127.0.0.1:8000"


export async function getAllTemperature() {
    const response =  await fetch(url + "/allTemperature")
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async function getTemperatureByTime(time) {
    const response =  await fetch(url + "/temperatureTime/" + time)
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async function getTemperatureBySensor(sensor_name) {
    const response =  await fetch("/temperatureSensor/" + sensor_name)
    if (!response.ok){
        return null
    }
    return await response.json()
}


export async  function getAlert(){
    const response = await fetch(`${url}/getAlert`)
    if(!response.ok){
        return null
    }
    return await response.json()
}

export async function postTemperatureAlert(alertTemperature){
    await fetch(`${url}/setAlert`,{
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