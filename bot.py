import os

import telebot
import aiogram
import re

def extract_hashtags(text):
    return re.findall(r'#\w+', text)
# List of options
startOptions = ['Tạo Chuyến mới ngày hôm nay', 'Cập nhật thông tin ']
options = ["Option 1", "Option 2", "Option 3"]


BOT_TOKEN = '7532790137:AAGZp9D99gtFUykO92wshQAynp3UWtdba-I'
bot = telebot.TeleBot(BOT_TOKEN)
@bot.message_handler(func=lambda message: '#' in message.text)
def handle_hashtags(message):
    hashtags = extract_hashtags(message.text)
    if hashtags:
        # Process the extracted hashtags (e.g., store them, analyze, etc.)
        response = f"Received hashtags: {', '.join(hashtags)}"
        hashtag_text = message.text.split('#', 1)[-1].strip()

        # Generate hashtag suggestions (you can customize this logic)
        suggested_hashtags = ["#python", "#programming", "#telegram", "#bots"]

        # Respond with the suggestions
        if hashtag_text:
            response = f"Suggested hashtags for '{hashtag_text}': {', '.join(suggested_hashtags)}"
        else:
            response = "Please type a keyword after the '#' symbol."
    else:
        response = "No hashtags found in the message."
        
    bot.reply_to(message, response)
@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text

    # Print the message contents
    print(f"Chat ID: {chat_id}, User ID: {user_id}, Message: {text}")
    markup = telebot.types.InlineKeyboardMarkup()
    for option in startOptions:
        button = telebot.types.InlineKeyboardButton(option, callback_data=option)
        markup.add(button)
    bot.send_message(message.chat.id, "Chọn chức năng", reply_markup=markup)
    
    bot.reply_to(message, "Howdy, how are you doing?")
    

@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    text = message.text

    # Print the message contents
    print(f"Chat ID: {chat_id}, User ID: {user_id}, Message: {text}")
    bot.reply_to(message,f"Chat ID: {chat_id}, User ID: {user_id}, Message: {text} Welcome! Use /select to choose an option.")

@bot.message_handler(commands=['select'])
def handle_select(message):
    markup = telebot.types.InlineKeyboardMarkup()
    for option in options:
        button = telebot.types.InlineKeyboardButton(option, callback_data=option)
        markup.add(button)
    bot.send_message(message.chat.id, "Select an option:", reply_markup=markup)
    
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    # Your custom logic here
    bot.reply_to(message, "Received a text message!")
    
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    selected_option = call.data
    bot.answer_callback_query(call.id, f"You selected: {selected_option}")
    
bot.infinity_polling()
# if __name__ == "__main__":
#     bot.polling()