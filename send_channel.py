import requests
import telebot

BOT_TOKEN = "6215098672:AAF6Hs82QQ4kD_KFEFthSc_Qer6JHZEbipQ"
bot = telebot.TeleBot(BOT_TOKEN)

# Thay thế 'YOUR_API_KEY' bằng khóa API của bạn từ CoinMarketCap
api_key = '163fefc4-0c69-4d35-9885-b1a975dc55eb'

def send_channel_price_up():
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=200&CMC_PRO_API_KEY={api_key}'

    # Gửi yêu cầu GET đến API của CoinMarketCap
    response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công (status code 200)
    if response.status_code == 200:
        # Lấy dữ liệu JSON từ phản hồi
        data = response.json()

        # Sắp xếp danh sách các đồng tiền theo tỷ lệ tăng giá trong 24 giờ
        sorted_coins = sorted(data['data'], key=lambda x: x['quote']['USD']['percent_change_24h'], reverse=True)

        # Lấy danh sách 5 đồng tiền tăng giá nhiều nhất
        top_5_coins = sorted_coins[:5]

        msg = "Top 5 đồng tiền tăng giá nhiều nhất trong 24 giờ gần đây:\n\n"
        for coin in top_5_coins:
            symbol = coin['symbol']
            price = coin['quote']['USD']['price']
            price_formatted = "{:.2f}".format(price)
            price_change_24h = coin['quote']['USD']['percent_change_24h']
            price_change_24h_formatted = "{:.2f}".format(price_change_24h)
            msg += f'{symbol} : ${price_formatted}(🟢{price_change_24h_formatted}%)\n'
        bot.send_message("@TAxCAPITAL",msg,parse_mode="Markdown")
        
    else:
        bot.send_message(1338012419,"Không thể kết nối đến CoinMarketCap API.",parse_mode="Markdown")

def send_channel_price_down():
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=200&CMC_PRO_API_KEY={api_key}'

    # Gửi yêu cầu GET đến API của CoinMarketCap
    response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công (status code 200)
    if response.status_code == 200:
        # Lấy dữ liệu JSON từ phản hồi
        data = response.json()

        # Sắp xếp danh sách các đồng tiền theo tỷ lệ giảm giá trong 24 giờ
        sorted_coins = sorted(data['data'], key=lambda x: x['quote']['USD']['percent_change_24h'])

        # Lấy danh sách 5 đồng tiền giảm giá nhiều nhất
        top_5_coins = sorted_coins[:5]

        # In danh sách các đồng tiền giảm giá nhiều nhất ra màn hình
        msg = "Top 5 đồng tiền giảm giá nhiều nhất trong 24 giờ gần đây:\n\n"
        for coin in top_5_coins:
            symbol = coin['symbol']
            price = coin['quote']['USD']['price']
            price_formatted = "{:.2f}".format(price)
            price_change_24h = coin['quote']['USD']['percent_change_24h']
            price_change_24h_formatted = "{:.2f}".format(price_change_24h)
            msg += f'{symbol} : ${price_formatted}(🔴{price_change_24h_formatted}%)\n'
        bot.send_message("@TAxCAPITAL",msg,parse_mode="Markdown")           
            
    else:
        bot.send_message(1338012419,"Không thể kết nối đến CoinMarketCap API.",parse_mode="Markdown")       