from telegram.ext import CommandHandler , MessageHandler ,Updater
from telegram import ReplyKeyboardMarkup , keyboardbutton
from telegram import InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext.filters import Filters
import time
from telegram.chataction import ChatAction
import wikipedia
import requests

updater = Updater('5000124728:AAFFQSfSGqQFCvj5bJeWFVP0e9JCo7Sd-Ns')
my_chat_id = 1087559057

def start(update , context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    context.bot.sendMessage(my_chat_id, '{} {} with usernam:({}) has started robot'.format(user['first_name'],user['last_name'],user['username']))
    rpmks = [['ارتبات با من '],]
    context.bot.sendMessage(chat_id,'سلام {} {} به ربات علیرضا رضایی با من خوش امدید.'.format(user['first_name'],user['last_name']), reply_markup = ReplyKeyboardMarkup(rpmks))

def favor(update , context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    keyboards = [
        [InlineKeyboardButton('رفتن به سایت من ','https://alirezarezaei.pythonanywhere.com')],
        [InlineKeyboardButton('ارتبات با من در تلگرام ','https://t.me/a8888ralireza')]
    ]
    context.bot.sendMessage(chat_id,'چه کاری میتونم براتون انجام بدم؟',reply_markup = InlineKeyboardMarkup(keyboards))

    context.bot.sendMessage(my_chat_id, '{} {} with usernam:({}) has seen ertebat ba man'.format(user['first_name'],user['last_name'],user['username']))

def jan(update , context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.sendMessage(chat_id,'جان ربات؟')


def about(update , context):
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    msg = update.message.text
    title = msg.replace('درباره' , '')
    wikipedia.set_lang('fa')
    r = wikipedia.summary(title)
    update.message.reply_text(r)
    context.bot.sendMessage(my_chat_id, '{} {} with usernam:({}) has seen wikipedia for ({})'.format(user['first_name'],user['last_name'],user['username'],title))
    
def term(update,context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    msg = update.message.text
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    title = msg.replace('اصطلاح' , '')
    url = 'https://www.dictionaryapi.com/api/v3/references/medical/json/{}?key=7e92201a-48a3-4983-afea-da6583d565ef'.format(title)
    r = requests.get(url)
    data = r.json()
    try:
        mozo = data[0]['meta']['id']
        talf = data[0]['hwi']['prs'][0]['mw']
        mortabets = data[0]['meta']['stems']
        mortabet = ''
        for i in mortabets:
            mortabet = mortabet + ' ' + i
        manis = data[0]['shortdef']
        mani = ''
        for i in manis:
            mani = mani + i + '\n'
    
        mess = 'اصطلاح:{}\n تلفظ:{} \n کلمات مرتبط:{} \n معانی:{} \n پرسش از :{}'.format(mozo,talf,mortabet,mani,user['first_name'])
        context.bot.sendMessage(my_chat_id, mess + '\n from : {}'.format(user['username']))
        update.message.reply_text(mess)

    except TypeError:
        update.message.reply_text('متاسفانه کلمه ی مورد نظر شما در دیکشنری ما یافت نشد!')



#handelers
start_hand = CommandHandler('start',start)
jan_hand = MessageHandler(Filters.regex('ربات'),jan)
about_hand = MessageHandler(Filters.regex(r'ربات درباره'),about)
about2_hand = MessageHandler(Filters.regex(r'درباره'),about)
term_hand = MessageHandler(Filters.regex(r'اصطلاح'),term)
term2_hand = MessageHandler(Filters.regex(r'اصطلاح'),term)
favor_command = MessageHandler(Filters.regex(r'ارتباط با من'),favor)

dis = updater.dispatcher
dis.add_handler(start_hand)
dis.add_handler(jan_hand)
dis.add_handler(about_hand)
dis.add_handler(about2_hand)
dis.add_handler(term_hand)
dis.add_handler(term2_hand)
dis.add_handler(favor_command)





updater.start_polling()
updater.idle()