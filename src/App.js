import logo from './logo.svg';
import './App.css';
import ChartCard from './component/cart/chartCard';
import React, {useEffect, useState } from "react";
import { BrowserRouter as Router, useRoutes, Link } from 'react-router-dom';
import Header from './component/header/header';
import Home from './component/home/home';
import { Button } from '@mui/material';

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

       <div className='body'>
        <Header/>
         <Button onClick={toggle} variant="outlined"  sx={{
    '&:hover': {
      backgroundColor: '#282c34',
      color:"#F5DEB3"
    },
  }}>
                {isOn ? 'Influx' : 'Oracle'}
        </Button>
        
        
    </div>
        <AppRoutes/>

    </>
   
   
    );
}

export default App;
