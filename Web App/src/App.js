import {Routes, Route, useLocation} from "react-router-dom"
import Products from "./routes/Products"
import Shipping from "./routes/Shipping"
import NoMatch from "./routes/NoMatch"
import Basket from "./routes/Basket"
import Home from "./routes/Home"
import menu from './menu'
import './css/App.css'
import tg from "./telegram/main"
import closeImage from "./closeImageFunc"
import homePageReroute from "./RerouteFunc"

function App() {
  const location = useLocation()
  return (
    <>
      <div id="image-loader" onClick={event => {
        if (location.pathname === '/') tg.BackButton.hide()
        tg.BackButton.offClick(closeImage)
        tg.BackButton.onClick(homePageReroute)

        document.getElementsByTagName('body')[0].style.overflow = 'auto'
        event.target.style.backgroundImage = 'none'
        event.target.style.display = 'none'
        }}></div>
      <div className="middle-container">
        <Routes>
          <Route index element={<Home groups={menu}/>} />
          <Route path="/" element={<Home groups={menu}/>} />
          <Route path="products" element={<Products />}/>
          <Route path="basket" element={<Basket />}/>
          <Route path="payment" element={<Shipping/>}/>
          <Route path='*' element={<NoMatch/>}/>
        </Routes>
      </div>
    </>
  );
}

export default App;
