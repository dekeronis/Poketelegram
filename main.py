import telebot 
from config import token

from logic import Pokemon, get_pokemon

bot = telebot.TeleBot(token) 

@bot.message_handler(commands=['go'])
def go(message):
    user_id = message.from_user.id
    if user_id not in Pokemon.pokemons:
        pokemon = Pokemon(user_id)
        bot.send_message(message.chat.id, pokemon.info())
        bot.send_message(message.chat.id, f"Тип: {pokemon.data['type']}")
        bot.send_photo(message.chat.id, pokemon.show_img())
    else:
        bot.reply_to(message, "Ты уже создал себе покемона")


@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.from_user.id
    p = get_pokemon(user_id)

    if not p:
        bot.reply_to(message, "У тебя нет покемона. Используй /go")
        return

    bot.send_message(message.chat.id, p.info())
    bot.send_photo(message.chat.id, p.show_img())

@bot.message_handler(commands=['train'])
def train(message):
    user_id = message.from_user.id
    p = get_pokemon(user_id)

    if not p:
        bot.reply_to(message, "Сначала создай покемона через /go")
        return

    leveled = p.add_xp(10)

    if leveled:
        bot.reply_to(message, f"Тренировка успешна! {p.data['name']} получил новый уровень {p.level}!")
    else:
        bot.reply_to(message, f"{p.data['name']} потренировался и получил 10 XP!")


bot.infinity_polling(none_stop=True)

