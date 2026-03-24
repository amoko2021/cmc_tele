import requests
import telebot
import os
from dotenv import load_dotenv

load_dotenv()

bot = telebot.TeleBot(os.getenv("TOKEN"))

# Thay thế 'YOUR_API_KEY' bằng khóa API của bạn từ CoinMarketCap
api_key = os.getenv("KEY_CMC")


def get_price(name,id, id_message): # lấy giá BTC
   # Tên của đồng tiền mã hóa bạn muốn lấy giá (ví dụ: Bitcoin là 'bitcoin', Ethereum là 'ethereum')
    coin_name = str(name)

    # Tạo URL cho yêu cầu API
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?symbol={coin_name.upper()}&CMC_PRO_API_KEY={api_key}'

    # Gửi yêu cầu GET đến API của CoinMarketCap
    response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công (status code 200)
    if response.status_code == 200:
        # Lấy dữ liệu JSON từ phản hồi
        data = response.json()

        # Trích xuất giá của đồng tiền mã hóa từ dữ liệu JSON
        price = data['data'][coin_name.upper()]['quote']['USD']['price']

        # In giá ra màn hình
        #print(f'Giá của {coin_name.upper()} là ${int(price)}')
        # Gửi lên tele
        # bot.send_message(id, f'Giá của {coin_name.upper()} là ${int(price)}')
        bot.edit_message_text(f'Giá của {coin_name.upper()} là ${int(price)}', id, id_message, 
                              reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Quay lại', callback_data='back')))
        # print(data)
    else:
        #print('Không thể kết nối đến CoinMarketCap API.')
        bot.send_message(id, 'Không thể kết nối đến CoinMarketCap API.')

def get_top_coin_up_24h(id, id_message): # lấy giá 5 coin (từ top1 đến top 1000) tăng giá nhiều nhất trong 24h
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=1000&CMC_PRO_API_KEY={api_key}'

    # Gửi yêu cầu GET đến API của CoinMarketCap
    response = requests.get(url)

    # Kiểm tra nếu yêu cầu thành công (status code 200)
    if response.status_code == 200:
        # Lấy dữ liệu JSON từ phản hồi
        data = response.json()

        # Sắp xếp danh sách các đồng tiền theo tỷ lệ tăng giá trong 24 giờ
        sorted_coins = sorted(data['data'], key=lambda x: x['quote']['USD']['percent_change_24h'], reverse=True)
      #  print(data)
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
        bot.edit_message_text(msg, id, id_message, parse_mode="Markdown",
                              reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Quay lại', callback_data='back')))    
    else:
        print('Không thể kết nối đến CoinMarketCap API.')    

def get_top_coin_down_24h(id, id_message): # lấy giá 5 coin (từ top1 đến top 1000) giảm giá nhiều nhất trong 24h
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=1000&CMC_PRO_API_KEY={api_key}'

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
        bot.edit_message_text(msg, id, id_message, parse_mode="Markdown",
                              reply_markup=telebot.types.InlineKeyboardMarkup().add(telebot.types.InlineKeyboardButton('Quay lại', callback_data='back')))               
            
    else:
        print('Không thể kết nối đến CoinMarketCap API.')    
