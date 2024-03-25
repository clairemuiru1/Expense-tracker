import React, { useState } from 'react'
import { Routes, Route } from 'react-router-dom'
import Signin from './components/Signin/Signin'
import Navbar from './components/Navbar/Navbar'
import Home from './Pages/Home/Home'
import Bills from './Pages/Bills/Bills'
import Categories from './Pages/Categories/Categories'
import Payments from './Pages/Payments/Payments'
import Footer from './components/Footer/Footer'

function App() {

  const [showLogin,setShowLogin] = useState(false)

  return (
    <>
      {showLogin? <Signin  setShowLogin={setShowLogin}/>: <></>}
      <div className='app'>
        <Navbar setShowLogin={setShowLogin}/>
        <Routes>
          <Route path='/' element={<Home />} />
          <Route path='/bills' element={<Bills />} />
          <Route path='/categories' element={<Categories />} />
          <Route path='/payments' element={<Payments />} />
        </Routes>
      </div>
      <Footer />
    </>
  )
}

export default App
