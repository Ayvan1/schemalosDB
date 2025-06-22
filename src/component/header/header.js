import React from "react";
import { Link } from "react-router-dom";

function Header(){
    
    return(
        <header>
            <h1>
                CPU Monitoring
            </h1>
            
            <nav>
                <Link to="/">Home</Link>
                <Link to="/ChartCart">Monitoring</Link>
            </nav>
        </header>
    )
}

export default Header