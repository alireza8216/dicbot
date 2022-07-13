from telegram.ext import CommandHandler , MessageHandler ,Updater 
from telegram import ReplyKeyboardMarkup , keyboardbutton
from telegram import InlineKeyboardButton , InlineKeyboardMarkup
from telegram.ext.filters import Filters
from telegram.chataction import ChatAction
import wikipedia
import requests
import os 
from translate import Translator

#inlinequery libraries
from telegram.ext import InlineQueryHandler
from telegram import InputTextMessageContent
from telegram import InlineQueryResultArticle
from uuid import uuid4

TOKEN = '5000124728:AAFFQSfSGqQFCvj5bJeWFVP0e9JCo7Sd-Ns'
updater = Updater('5000124728:AAFFQSfSGqQFCvj5bJeWFVP0e9JCo7Sd-Ns')
my_chat_id = 1087559057

def start(update , context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    context.bot.sendMessage(my_chat_id, '{} {} with usernam:({}) has started robot'.format(user['first_name'],user['last_name'],user['username']))
    rpmks = [['ارتباط با من '],['راهنما']]
    context.bot.sendMessage(chat_id,'سلام {} {} به ربات علیرضا رضایی با من خوش امدید.'.format(user['first_name'],user['last_name']), reply_markup = ReplyKeyboardMarkup(rpmks))

def favor(update , context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    keyboards = [
        [InlineKeyboardButton('رفتن به سایت من ','https://alirezarezaei.pythonanywhere.com')],
        [InlineKeyboardButton('ارتباط با من در تلگرام ','https://t.me/a8888ralireza')]
    ]
    context.bot.sendMessage(chat_id,'چه کاری میتونم براتون انجام بدم؟',reply_markup = InlineKeyboardMarkup(keyboards))

    context.bot.sendMessage(my_chat_id, '{} {} with usernam:({}) has seen ertebat ba man'.format(user['first_name'],user['last_name'],user['username']))

def helpp(update,context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    text1 = "با وارد کردن (اصطلاح... )میتواند معنی و تلفظ اصطلاح پزشکی مورد نظر را دریافت کنیم/n"
    text2 = "2.با وارد کردن (درباره ...) میتوانید در مورد ان کلمه  اطلاعات گوگل را دریافت کنید"
    text3 = "3.میتوانید با وارد کردن (ترجمه ...) متن انگلیسی مورد نظر خود را از انگلیسی به فارسی معنی کنید"
    text4 = "4.میتوانید با وارد کردن (مقاله ...) و شماره ی مقاله مقاله ی مورد نظر را از سایت من دریافت کنید"
    text5 = "5. میتوانید با وارد کردن (داستان کوتاه) به صورت رندوم یک داستان کوتاه دریافت کنید (:"
    text6 = "6. میتوانید با وارد کردن (ارتباط با من) با من ارتباط برقرار کنید"
    update.message.reply_text(text1+"\n"+text2+"\n"+text3+"\n"+text4+"\n"+text5+"\n"+text6)
    context.bot.sendMessage(my_chat_id, '{} {} with usernam:({}) has seen rahnama estefade'.format(user['first_name'],user['last_name'],user['username']))

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

def blog(update,context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    msg = update.message.text
    title = msg.replace('مقاله','')
    #if title.isdigit():
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    hi = int(title) - 1
    result = requests.get('https://alirezarezaei.pythonanywhere.com/blog/api/').json()
    try:
        article = result[hi]['fields']
        mozo = article['name']
        pic = 'https://alirezarezaei.pythonanywhere.com/media/'+article['pic']
        date = article['date']
        category = article['category']
        intro = article['intro']
        important = article['important']
        text1 = article['text1']
        text2 = article['text2']
        context.bot.sendMessage(my_chat_id,"{} {} with usernam:({}) has seen blog number ({})".format(user['first_name'],user['last_name'],user['username'],str(title)))
        context.bot.send_photo(chat_id,pic)
        update.message.reply_text('موضوع:{} \n تاریخ:{} \n کتگوری:{} \n متن:{} \n {} \n {} \n {}'.format(mozo,date,category,intro,important,text1,text2))
        update.message.reply_text('link:   https://alirezarezaei.pythonanywhere.com/blog/{}'.format(int(title)))
        
    except IndexError:
        update.message.reply_text('متاسفانه هنوز مقاله ی شماره {} نوشته نشده است'.format(str(title)))
    

def tarjom(update , context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    msg = update.message.text
    title = msg.replace("ترجمه",'')
    tl = Translator( to_lang='fa')
    fa = tl.translate(title)
    context.bot.sendMessage(my_chat_id,"{} {} with usernam:({}) has seen translation of ({})".format(user['first_name'],user['last_name'],user['username'],title))
    update.message.reply_text(fa)

def dastan(update,context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    context.bot.send_chat_action(chat_id,ChatAction.TYPING)
    result = requests.get('http://api.codebazan.ir/dastan/')
    update.message.reply_text(str(result.text))

#inline queries
def inline(update, context):
    global my_chat_id
    user = update.message.from_user
    chat_id = update.message.chat_id
    text = update.inline_query.query
    res = list()

    #about
    wiki = wikipedia.summary(text)

    #estelah
    url = 'https://www.dictionaryapi.com/api/v3/references/medical/json/{}?key=7e92201a-48a3-4983-afea-da6583d565ef'.format(text)
    api_estelah = requests.get(url)
    data = api_estelah.json()
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
    
    estelah = 'اصطلاح:{}\n تلفظ:{} \n کلمات مرتبط:{} \n معانی:{} \n پرسش از :{}'.format(mozo,talf,mortabet,mani,user['first_name'])

    #blogs
    num = text -1
    article_api = requests.get('https://alirezarezaei.pythonanywhere.com/blog/api/').json()

    article = article_api[num]['fields']
    mozo_blog = article['name']
    pic_blog = 'https://alirezarezaei.pythonanywhere.com/media/'+article['pic']
    date_blog = article['date']
    category_blog = article['category']
    intro_blog = article['intro']
    important_blog = article['important']
    text1_blog = article['text1']
    text2_blog = article['text2']
    blog = 'موضوع:{} \n تاریخ:{} \n کتگوری:{} \n متن:{} \n {} \n {} \n {}'.format(mozo_blog,date_blog,category_blog,intro_blog,important_blog,text1_blog,text2_blog)

    #tarjome
    tl = Translator( to_lang='fa')
    fa = tl.translate(text)

    #set inlines
    res.append(InlineQueryResultArticle(id=uuid4(), title='درباره ی این کلمه', input_message_content=InputTextMessageContent(wiki)))
    res.append(InlineQueryResultArticle(id=uuid4(), title='اصطلاح پزشکی', input_message_content=InputTextMessageContent(estelah)))
    res.append(InlineQueryResultArticle(id=uuid4(), title='مقاله به این شماره', input_message_content=InputTextMessageContent(blog)))
    res.append(InlineQueryResultArticle(id=uuid4(), title='ترجمش کن', input_message_content=InputTextMessageContent(fa)))
    
    #answer
    context.bot.answerInlineQuery(result = res)


#handelers
start_hand = CommandHandler('start',start)
jan_hand = MessageHandler(Filters.regex('^ربات$'),jan)
about_hand = MessageHandler(Filters.regex(r'ربات درباره'),about)
about2_hand = MessageHandler(Filters.regex(r'درباره'),about)
term_hand = MessageHandler(Filters.regex(r'اصطلاح'),term)
term2_hand = MessageHandler(Filters.regex(r'اصطلاح'),term)
favor_command = MessageHandler(Filters.regex(r'ارتباط با من'),favor)
favor2_command = MessageHandler(Filters.regex(r'ارتباط'),favor)
blog_hand = MessageHandler(Filters.regex("مقاله"),blog)
tarjom_hand = MessageHandler(Filters.regex('ترجمه'),tarjom)
dastan_hand = MessageHandler(Filters.regex('داستان کوتاه'),dastan)
help1_hand = MessageHandler(Filters.regex('راهنما'),helpp)
help2_hand = CommandHandler('help',helpp)
inline_hand = InlineQueryHandler(inline)


dis = updater.dispatcher
dis.add_handler(start_hand)
dis.add_handler(jan_hand)
dis.add_handler(about_hand)
dis.add_handler(about2_hand)
dis.add_handler(term_hand)
dis.add_handler(term2_hand)
dis.add_handler(favor_command)
dis.add_handler(favor2_command)
dis.add_handler(blog_hand)
dis.add_handler(tarjom_hand)
dis.add_handler(dastan_hand)
dis.add_handler(help1_hand)
dis.add_handler(help2_hand)
dis.add_handler(inline_hand)

PORT = int(os.environ.get('PORT', '8443'))

updater.start_webhook(
    listen="0.0.0.0",
    port=int(PORT),
    url_path=TOKEN,
    webhook_url='https://dicbotpython.herokuapp.com/' + TOKEN
)

#
#updater.start_polling()
updater.idle()
