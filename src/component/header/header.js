import React, { useState } from "react";

function Header(){
    const [isOn,setIsOn] = useState(false);
    const toggle = () => {
    setIsOn(prev => !prev);
    };
    return(
        <header>
            <h1>
                CPU Monitoring
            </h1>
            <button onClick={toggle}>
                {isOn ? 'Influx' : 'Oracle'}
            </button>
            <ul>
                <li>Monitoring</li>
                <li>Alert</li>
            </ul>
        </header>
    )
}

export default Header