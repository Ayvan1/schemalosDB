import logo from './logo.svg';
import './App.css';
import ChartCard from './component/cart/chartCard';
import React, {useEffect, useState } from "react";
import { BrowserRouter as Router, useRoutes, Link } from 'react-router-dom';
import Header from './component/header/header';
import Home from './component/cart/home/home';

function App() {
  const [isOn,setIsOn] = useState(true);
  const toggle = () => {
          setIsOn(prev => !prev);
          console.log(isOn.valueOf())
  };

  const AppRoutes = () =>{
    const routes = useRoutes([
      {path:'/',element:<Home/>},
      {path: '/ChartCart', element:<ChartCard connectionDB={isOn} />}
    ])
    return routes
  }

  return (
    <>
        <Header/>
         <button onClick={toggle}>
                {isOn ? 'Influx' : 'Oracle'}
        </button>
        
        <AppRoutes/>
        
    </>
   
    );
}

export default App;
