import telebot

from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from get_price import get_price, get_top_coin_up_24h, get_top_coin_down_24h

import send_channel
import threading
import time
import os
from dotenv import load_dotenv

load_dotenv()

# def my_function():
#     # Hàm bạn muốn thực hiện lặp lại
#     print("Hello, world!")

# interval_seconds = 10  # Khoảng thời gian giữa mỗi lần gọi hàm (ví dụ: 10 giây)

# def repeat_function():
#     while True:
#         my_function()
#         time.sleep(interval_seconds)

# # Tạo một luồng (thread) để thực hiện hàm repeat_function()
# thread = threading.Thread(target=repeat_function)
# thread.start()

# Main thread tiếp tục thực hiện các công việc khác


bot = telebot.TeleBot(os.getenv("TOKEN")) # kết nối bot

def back_main(id, id_message): #Quay về main
    markups = InlineKeyboardMarkup()
    markups.add(InlineKeyboardButton("Check giá BTC", callback_data='price_btc'))
    markups.add(InlineKeyboardButton("Top coin up 24h", callback_data='top_coin_up'),
                InlineKeyboardButton("Top coin down 24h", callback_data='top_coin_down')
                )
    
    bot.edit_message_text("Chào mừng bạn đến với bot phát triển bởi TA Capital",id, id_message, reply_markup=markups)

@bot.message_handler(commands=['start'])
def welcome(message):
    markups = InlineKeyboardMarkup()
    markups.add(InlineKeyboardButton("Check giá BTC", callback_data='price_btc'))
    markups.add(InlineKeyboardButton("Top coin up 24h", callback_data='top_coin_up'),
                InlineKeyboardButton("Top coin down 24h", callback_data='top_coin_down')
                )
    markups.add(InlineKeyboardButton("Gửi tin nhắn lên kênh", callback_data='1send_channel'))
    bot.send_message(message.chat.id, "Chào mừng bạn đến với bot phát triển bởi TA Capital",reply_markup=markups)

@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.data == 'price_btc':
        get_price('btc', call.message.chat.id, call.message.message_id)
    if call.data == 'top_coin_up':
        get_top_coin_up_24h(call.message.chat.id, call.message.message_id)
    if call.data == 'top_coin_down':
       get_top_coin_down_24h(call.message.chat.id, call.message.message_id)    
    if call.data == 'back':
        back_main(call.message.chat.id, call.message.message_id)
    if call.data == '1send_channel':
        if call.message.chat.id == 1338012419:
            markups = InlineKeyboardMarkup()
            markups.add(InlineKeyboardButton("Top coin up 24h",callback_data="send:up"))
            markups.add(InlineKeyboardButton("Top coin down 24h",callback_data="send:down"))
            markups.add(InlineKeyboardButton("Quay lại",callback_data="back"))
            bot.edit_message_text("Vui lòng chọn tin nhắn muốn gửi", call.message.chat.id, call.message.message_id, reply_markup=markups)
        else:
            bot.send_message(call.message.chat.id, "Bạn không là admin.")        
    if call.data[:4] == "send":
        if call.data[5:] == "up":
            send_channel.send_channel_price_up()
        if call.data[5:] == "down":
            send_channel.send_channel_price_down()


if __name__ == '__main__': #chạy bot
    bot.infinity_polling()
