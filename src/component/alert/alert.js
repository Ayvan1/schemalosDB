import React, { useEffect, useState } from "react";
import ShowAlertComponent from "./showAlertComponent";
import SetAlertComponent from "./setAlertComponent";
import "./alert.css"


function Alert({connectionDB}){
   return(
    <div className="alert">
    <SetAlertComponent connectionDB={connectionDB}/>
    <ShowAlertComponent connectionDB={connectionDB}/>
    </div>
   )
} 

export default Alert;