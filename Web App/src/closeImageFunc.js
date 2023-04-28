import homePageReroute from "./RerouteFunc"
import tg from "./telegram"

function closeImage() {
    document.getElementById('image-loader').style.display = 'none'
    document.getElementById('image-loader').style.backgroundImage = 'none'
    document.getElementsByTagName('body')[0].style.overflow = 'auto'
    tg.BackButton.offClick(closeImage)
    tg.BackButton.onClick(homePageReroute)
    if (!document.getElementsByClassName('card-price')[0]) tg.BackButton.hide()
}

export default closeImage