import React from "react";
import { Link } from "react-router-dom";
import './header.css'

function Header(){
    
    return(
        <header>
            <img src="logo.svg" alt=""/>
            <nav>
                {/* <div>
                    <Link to="/" className="link">Home</Link>
                </div> */}
                <div>
                    <Link to="/" className="link">Monitoring</Link> 
                </div>
                 <div>
                    <Link to="/Alert" className="link">Alert</Link>
                </div>
            </nav>
        </header>
    )
}

export default Header