import homePageReroute from '../RerouteFunc'

let tg = window.Telegram.WebApp

tg.MainButton.color = '#FFBF00'
tg.MainButton.textColor = '#000000'

tg.BackButton.onClick(homePageReroute)

export default tg