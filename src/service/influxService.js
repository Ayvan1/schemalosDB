const url = "http://127.0.0.1:8000"


export async function getAllTemperature() {
    const response =  await fetch(url+"/all_temperature")
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async function getTemperatureByTime(time) {
    const response =  await fetch(url + "/temperature_time/" + time)
    if (!response.ok){
        return null
    }
    return await response.json()
}

export async function getTemperatureBySensor(sensor_name) {
    const response =  await fetch("/temperature_sensor/" + sensor_name)
    if (!response.ok){
        return null
    }
    return await response.json()
}