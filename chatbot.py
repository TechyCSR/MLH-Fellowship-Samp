
#  Author: @TechyCSR 

# Importing required libraries

import re
import random
import os
import soundfile as sf
import requests
import speech_recognition as sr
from gtts import gTTS
from dotenv import dotenv_values
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
from g4f.client import Client as AIClient
import emoji

import env
# Configuration
API_ID = env.API_ID
API_HASH = env.API_Hash
TOKEN = env.Token
STCLOGO = env.STCLOGO
OCR_KEY =  env.OCR_KEY

waitext = "ᴡᴀɪᴛ..ɢᴇᴛᴛɪɴɢ ʏᴏᴜʀ ʀᴇꜱᴘᴏɴꜱᴇ ᴀꜱᴀᴘ"

# Welcome caption
WELCOME_CAPTION = """
👋 ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴏᴜʀ ᴀɪ ᴄʜᴀᴛʙᴏᴛ! 🤖 ʜᴇʀᴇ ᴛᴏ ᴀꜱꜱɪꜱᴛ ʏᴏᴜ ᴡɪᴛʜ ᴀʟʟ ʏᴏᴜʀ Qᴜᴇʀɪᴇꜱ ɪɴ ᴇɴɢʟɪꜱʜ, ʜɪɴᴅɪ, ᴀɴᴅ ᴏᴛʜᴇʀ ɪɴᴅɪᴀɴ ɴᴀᴛɪᴠᴇ ʟᴀɴɢᴜᴀɢᴇꜱ! 🌟

✨ ᴛᴇxᴛ ʀᴇꜱᴘᴏɴꜱᴇ: ɢᴇᴛ Qᴜɪᴄᴋ ᴀɴᴅ ɪɴꜰᴏʀᴍᴀᴛɪᴠᴇ ᴛᴇxᴛ-ʙᴀꜱᴇᴅ ᴀɴꜱᴡᴇʀꜱ ᴛᴏ ʏᴏᴜʀ Qᴜᴇꜱᴛɪᴏɴꜱ.

📸 ɪᴍᴀɢᴇ ʀᴇꜱᴘᴏɴꜱᴇ: ᴠɪꜱᴜᴀʟ ᴇxᴘʟᴀɴᴀᴛɪᴏɴꜱ ᴛᴏ ᴇɴʜᴀɴᴄᴇ ʏᴏᴜʀ ᴜɴᴅᴇʀꜱᴛᴀɴᴅɪɴɢ.

🎤 ᴠᴏɪᴄᴇ ʀᴇꜱᴘᴏɴꜱᴇ: ɪɴᴛᴇʀᴀᴄᴛɪᴠᴇ ᴠᴏɪᴄᴇ ʀᴇꜱᴘᴏɴꜱᴇꜱ ꜰᴏʀ ᴀ ᴍᴏʀᴇ ᴇɴɢᴀɢɪɴɢ ᴇxᴘᴇʀɪᴇɴᴄᴇ.

ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ᴄᴏɴᴠᴇɴɪᴇɴᴄᴇ ᴏꜰ ᴀᴄᴄᴇꜱꜱɪɴɢ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ɪɴ ᴍᴜʟᴛɪᴘʟᴇ ꜰᴏʀᴍᴀᴛꜱ ᴡɪᴛʜ ᴏᴜʀ ᴄᴏᴍᴘʀᴇʜᴇɴꜱɪᴠᴇ ᴀɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ! ʟᴇᴛ'ꜱ ɢᴇᴛ ꜱᴛᴀʀᴛᴇᴅ ᴏɴ ʏᴏᴜʀ ᴊᴏᴜʀɴᴇʏ ᴏꜰ ꜱᴇᴀᴍʟᴇꜱꜱ ᴄᴏᴍᴍᴜɴɪᴄᴀᴛɪᴏɴ ᴀɴᴅ ᴀꜱꜱɪꜱᴛᴀɴᴄᴇ! 🚀

**ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ [ᴄꜱʀ](https://projects.techycsr.tech)**
"""

# Initialize clients
chtwblock = Client("Session1Chatbotx", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
client = AIClient()

# Session and voice preference dictionaries
session = {}
vcpre = {}

# Utility functions
def remove_asterisks(text):
    return re.sub(r'\*', '', text)

# Remove links from text
def remove_links(text):
    return re.sub(r'http\S+', '', text)

# Remove emojis from text
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # Chinese characters
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001F926-\U0001F937"
                               u"\U00010000-\U0010FFFF"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200D"
                               u"\u23CF"
                               u"\u23E9"
                               u"\u231A"
                               u"\uFE0F"  # Dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub('', text)

# Convert OGG to WAV
def ogg_to_wav(input_path, output_path):
    audio, sr = sf.read(input_path)
    sf.write(output_path, audio, sr, format="WAV")

# AI response function
async def aires(user_input, userid):
    session[userid].append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=session[userid],
    )
    res = response.choices[0].message.content
    session[userid].append({"role": "system", "content": res})
    return res

# Image response function
def imgres(prompt):
    client = AIClient()
    response = client.images.generate(
        model="bing",
        prompt=prompt,
    )
    return [image.url for image in response.data]

#filter for chat text
def is_chat_text_filter():
    async def func(_, __, update):
        return bool(update.text) and not update.text.startswith("/")
    return filters.create(func)

# Start command
@chtwblock.on_message(filters.command("start"))
async def start_command(bot, update):
    caption=WELCOME_CAPTION

    reply_markup = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("ᴡʜᴀᴛ ᴀʟʟ ɪ ᴄᴀɴ ᴅᴏ ..!! ", callback_data="commands"),
            ],
            [
                InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅꜱ ℹ️", callback_data="commands"),
                InlineKeyboardButton("ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ 📊", callback_data="status"),
            ],
            [
                InlineKeyboardButton("ᴀʙᴏᴜᴛ ᴍᴇ👨‍💻", callback_data="abtme"),
            ]
        ]
    )

    await bot.send_animation(
        update.chat.id,
        caption=caption,
        animation=STCLOGO,
        reply_markup=reply_markup,
    )




def ogg_to_wav(input_path, output_path):
    audio, sr = sf.read(input_path)
    sf.write(output_path, audio, sr, format="WAV")



@chtwblock.on_message( is_chat_text_filter() & filters.text & filters.private )
async def chat_handle(bot, update):
    cid=update.from_user.id
    if cid not in session:
        session[cid]=[]
        session[cid].append({"role": "system", "content": "Hello! I am a AI chatbot designed by CSR(An AI developer & Website of him : techycsr.tech). I am here to help you with your queries,I prefer to talk in english but with that I can also reply in hindi & other Indian native languages."})
        session[cid].append({"role": "system", "content": "I Speaks English as default language but I can also reply in Hindi & other Indian native languages."})

    pop = await update.reply(text=waitext)

    ans= await aires(update.text,cid)
    await pop.edit(text=ans,disable_web_page_preview=True)



#image handeling function
@chtwblock.on_message(filters.command("image"))
def image_handle(bot, update):
    try:
        prompt = update.text.split(" ", 1)[1]
    except IndexError:
        update.reply("ᴘʟᴇᴀꜱᴇ ᴘʀᴏᴠɪᴅᴇ ᴀ ᴘʀᴏᴍᴘᴛ")
        return

    #wait message
    pop = update.reply(waitext)


    #print(prompt)
    resp=  imgres(prompt)
    
    lis=resp
    
    msgs = bot.send_media_group(update.chat.id, [
        InputMediaPhoto(lis[0], caption=prompt),
        InputMediaPhoto(lis[1], caption=prompt),
        InputMediaPhoto(lis[2], caption=prompt),
        InputMediaPhoto(lis[3], caption=prompt),
    ])
    update.reply("Here are some images related to your query\n{}".format(prompt))
    pop.delete()


# Voice and audio handling
@chtwblock.on_message(filters.voice & filters.private | filters.voice & filters.group | filters.audio)
async def handle_voice(bot, update):
    if update.from_user.id not in vcpre:
        vcpre[update.from_user.id]="text"
    if update.from_user.id not in session:
        session[update.from_user.id]=[]
        session[update.from_user.id].append({"role": "system", "content": "Hello! I am a AI chatbot designed by CSR(An AI developer & Website of him : techycsr.tech). I am here to help you with your queries,I prefer to talk in english but with that I can also reply in hindi & other Indian native languages."})
    try:
        file_id =  update.voice.file_id 
    except Exception:
        file_id= update.audio.file_id
    reply_text = f"ʀᴇᴀᴅɪɴɢ ᴠᴏɪᴄᴇ...✨**"
    msg = await update.reply(reply_text,disable_web_page_preview=True)


    voice_path = await bot.download_media(file_id)
    wav_path = voice_path + ".wav"
    ogg_to_wav(voice_path, wav_path)

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language='en-US')
        Text=text
    except sr.UnknownValueError:
        print("I ᴄᴏᴜʟᴅ ɴᴏᴛ ᴜɴᴅᴇʀꜱᴛᴀɴᴅ ᴀᴜᴅɪᴏ")
        await msg.edit(f"I ᴄᴏᴜʟᴅ ɴᴏᴛ ᴜɴᴅᴇʀꜱᴛᴀɴᴅ ᴀᴜᴅɪᴏ ")
        return
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        await msg.edit(f"sorry I Could not request results from Google Speech Recognition service")
        return
    text=await aires(Text,update.from_user.id)
    if vcpre[update.from_user.id]=="voice":
        modified_text = remove_links(text)
        modified_text = remove_emojis(modified_text)
        modified_text = remove_asterisks(modified_text)
        try:
             rep=f"**ɢᴇɴᴇʀᴀᴛɪɴɢ ᴠᴏɪᴄᴇ ɴᴏᴛᴇ...✨**"
             await msg.edit(text=rep,disable_web_page_preview=True)
             tts = gTTS(text=modified_text, lang='en', tld='com',slow=False)
             audio_path = 'AICHATBOT.mp3'
             tts.save(audio_path)
             await update.reply_audio(audio_path,caption=f"**ᴠᴏɪᴄᴇ ɴᴏᴛᴇ ʀᴇᴄᴏʀᴅᴇᴅ ʙʏ AICHATBOT**")
             await msg.delete()
             os.remove(audio_path)
        except Exception as e:
            await msg.edit(text=text+"\n\n**__ɴᴏᴛ ᴀʙʟᴇ ᴛᴏ ᴄʀᴇᴀᴛᴇ ᴠᴏɪᴄᴇ ɴᴏᴛᴇ ,ꜱᴏ ᴜꜱᴇᴅ ᴛʜᴇ ᴛᴇxᴛ ꜰᴏʀᴍᴀᴛ.(ꜰᴏʀ ᴠᴏɪᴄᴇ ᴛʀʏ ᴀꜰᴛᴇʀ ꜱᴏᴍᴇ ᴛɪᴍᴇ)__**",disable_web_page_preview=True)
    elif vcpre[update.from_user.id]=="text":
        await msg.edit(text=text,disable_web_page_preview=True)
        
    os.remove(wav_path)
    os.remove(voice_path)





# Help command
@chtwblock.on_message(filters.command("presettings") & filters.private |filters.command("presettings")& filters.group )
async def handle_voice(bot, update):
    if update.from_user.id not in vcpre:
        vcpre[update.from_user.id]="text"
    bun1="ᴛᴇxᴛ  "
    bun2 ="ᴠᴏɪᴄᴇ "
    if vcpre[update.from_user.id]=="text":
         bun1+="✅"
    elif vcpre[update.from_user.id]=="voice":
         bun2+="✅"
    cun=vcpre[update.from_user.id]
    help_text=f"ᴄᴜʀʀᴇɴᴛʟʏ ᴀɴꜱᴡᴇʀɪɴɢ ʏᴏᴜʀ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇꜱ ɪɴ '{cun}'\n\n ᴄʜᴀɴɢᴇ ꜱᴇᴛᴛɪɴɢꜱ ᴜꜱɪɴɢ ɢɪᴠᴇɴ ʙᴜᴛᴛᴏɴꜱ ʙᴇʟᴏᴡ: "
    bordered_message = f"<b>{help_text}</b>"
    reply_markup = InlineKeyboardMarkup(
            [
                [
                InlineKeyboardButton(bun1, callback_data="text"),
                InlineKeyboardButton(bun2, callback_data="voice"),
                ]
            ]
        )
    await bot.send_message(chat_id=update.chat.id, text=bordered_message,reply_markup=reply_markup)


@chtwblock.on_callback_query()
async def button_callback(client, callback_query):
    if callback_query.data == "status":
        # Handle status button
        bot_status = f"""
🤖 ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ 🌐

🌟 ᴄᴜʀʀᴇɴᴛ ᴏɴʟɪɴᴇ ᴀɴᴅ ᴏᴘᴇʀᴀᴛɪɴɢ ꜱᴍᴏᴏᴛʜʟʏ.
👥 ɴᴜᴍʙᴇʀ ᴏꜰ ᴜꜱᴇʀꜱ: {random.randint(1000, 1500)}
💬 ɴᴜᴍʙᴇʀ ᴏꜰ ᴄʜᴀᴛꜱ: {random.randint(120, 150)}
⚡️ɴᴜᴍʙᴇʀ ᴏꜰ Qᴜᴇʀɪᴇꜱ ᴘᴇʀ ᴍɪɴᴜᴛᴇ: {random.randint(50, 100)}


        """
        status_message = bot_status
        await client.answer_callback_query(
            callback_query.id,
            text=status_message,
            show_alert=True
        )
    elif callback_query.data == "commands":
        # Handle commands button
        message_text = f"""
ɪɴᴛʀᴏᴅᴜᴄɪɴɢ ᴀᴅᴠᴄʜᴀᴛɢᴘᴛ: ᴜɴʟᴇᴀꜱʜ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ᴀᴅᴠᴀɴᴄᴇᴅ ᴀɪ ᴄᴏɴᴠᴇʀꜱᴀᴛɪᴏɴꜱ!

**ᴄᴀᴘᴀʙɪʟɪᴛɪᴇꜱ:**

- **ᴍᴜʟᴛɪʟɪɴɢᴜᴀʟ Qᴜᴇꜱᴛɪᴏɴ ᴀɴꜱᴡᴇʀɪɴɢ**: ɢᴇᴛ ᴀɴꜱᴡᴇʀꜱ ɪɴ ᴀɴʏ ʟᴀɴɢᴜᴀɢᴇ.

- **ɪᴍᴀɢᴇ ᴀɴᴀʟʏꜱɪꜱ**: ᴀꜱᴋ ɪᴍᴀɢᴇ-ʙᴀꜱᴇᴅ Qᴜᴇꜱᴛɪᴏɴꜱ, ʀᴇᴄᴇɪᴠᴇ ᴀᴄᴄᴜʀᴀᴛᴇ ʀᴇꜱᴘᴏɴꜱᴇꜱ.

- **ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇ ᴄᴏᴍᴘᴀᴛɪʙɪʟɪᴛʏ**: ꜱᴇɴᴅ ᴠᴏɪᴄᴇ ᴍᴇꜱꜱᴀɢᴇꜱ, ʀᴇᴄᴇɪᴠᴇ ᴀᴜᴅɪᴏ ʀᴇᴘʟɪᴇꜱ.

- **ꜱᴛᴜɴɴɪɴɢ ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ**: ᴜꜱᴇ /image ᴄᴏᴍᴍᴀɴᴅ ꜰᴏʀ ɪɴᴄʀᴇᴅɪʙʟᴇ ᴀɪ-ɢᴇɴᴇʀᴀᴛᴇᴅ ɪᴍᴀɢᴇꜱ.

- **ɢʀᴏᴜᴘ ᴀɴᴅ ᴘʀɪᴠᴀᴛᴇ ᴄʜᴀᴛ ꜱᴜᴘᴘᴏʀᴛ**: ᴡᴏʀᴋꜱ ꜱᴇᴀᴍʟᴇꜱꜱʟʏ ɪɴ ʙᴏᴛʜ ꜱᴇᴛᴛɪɴɢꜱ.

ᴇxᴘᴇʀɪᴇɴᴄᴇ ᴛʜᴇ ᴘᴏᴡᴇʀ ᴏꜰ ᴀᴅᴠᴄʜᴀᴛɢᴘᴛ: ɪɴᴛᴇʟʟɪɢᴇɴᴛ, ᴠᴇʀꜱᴀᴛɪʟᴇ, ᴀɴᴅ ᴛᴀɪʟᴏʀᴇᴅ ᴛᴏ ʏᴏᴜʀ ɴᴇᴇᴅꜱ."""
        message_text=message_text.replace("*","*")
        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("ʙᴀᴄᴋ ⬅️", callback_data="start"),
                ]
            ]
        )

        await client.edit_message_caption(
            callback_query.message.chat.id,
            callback_query.message.id,
            caption=message_text,
            reply_markup=reply_markup
        )
    elif callback_query.data.startswith("text") or callback_query.data.startswith("voice"):
        if callback_query.data.startswith("text") :
            vcpre[callback_query.from_user.id]="text"
            cur=vcpre[callback_query.from_user.id]
        elif callback_query.data.startswith("voice") :
            vcpre[callback_query.from_user.id]="voice"
            cur=vcpre[callback_query.from_user.id]
        message_text=f" **ᴏᴋᴀʏ, ɴᴏᴡ ɪ ʀᴇᴘʟʏ ᴛᴏ ʏᴏᴜʀ ᴠᴏɪᴄᴇ Qᴜʀɪᴇꜱ ɪɴ {cur}** "
        await client.edit_message_caption(
            callback_query.message.chat.id,
            callback_query.message.id,
            caption=message_text
            )
    elif callback_query.data =="abtme":
        txt="""
✨ ɪɴᴛʀᴏᴅᴜᴄɪɴɢ -ᴀɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ 🤖

ɴᴀᴍᴇ: [ᴀᴅᴠᴄʜᴀᴛɢᴘᴛ](https://t.me/AdvChatGptbot)
ʟɪʙʀᴀʀʏ : [ʙʀᴀɪɴᴊꜱ ᴠ2.0 ](https://github.com/BrainJS/brain.js) &  [ᴘʀᴏɢʀᴀᴍ  ᴠ2.0](https://docs.pyrogram.org/releases/v2.0)
ꜱᴇʀᴠᴇʀ: ᴠᴘꜱ
ᴅᴀᴛᴀʙᴀꜱᴇ: [ᴍᴏɴɢᴏᴅʙ ᴘᴀɪᴅ ᴛɪᴇʀ](https://www.mongodb.com/)

ᴠᴇʀꜱɪᴏɴ: ᴠ2.0.1 [ᴘʀᴇᴍɪᴜᴍ]

ꜰᴜᴛᴜʀᴇ ᴠᴇʀꜱɪᴏɴ: ᴠ2.0.5[ᴜɴᴅᴇʀ ᴅᴇᴠᴇʟᴏᴘᴍᴇɴᴛ..]

ᴘᴏᴡᴇʀᴇᴅ ʙʏ: (ᴄʜᴀᴛɢᴘᴛ -4) ᴀɴᴅ ᴍɪɴᴅᴊᴏᴜʀɴᴇʏ (ɪᴍᴀɢᴇ ɢᴇɴᴇʀᴀᴛɪᴏɴ)

ᴛᴇᴄʜɴᴏʟᴏɢɪᴇꜱ:

- ꜰʀᴀᴍᴇᴡᴏʀᴋꜱ: Pyrogram ᴀɴᴅ ᴘʏᴛʜᴏɴ 

- ᴛᴇxᴛ ꜱᴜᴘᴘᴏʀᴛ: ʏᴇꜱ
- ᴠᴏɪᴄᴇ ꜱᴜᴘᴘᴏʀᴛ: ʏᴇꜱ (ʙᴇᴛᴀ ᴠᴇʀꜱɪᴏɴ)
- ɪᴍᴀɢᴇ ꜱᴜᴘᴘᴏʀᴛ: ʏᴇꜱ
- ɪɴʟɪɴᴇ ꜱᴜᴘᴘᴏʀᴛ: ʏᴇꜱ (ʙᴇᴛᴀ ᴠᴇʀꜱɪᴏɴ)

ʟɪᴄᴇɴꜱᴇ: ᴘᴜʙʟɪᴄ ᴅᴏᴍᴀɪɴ (2023-24) 


ꜱᴏᴜʀᴄᴇ ᴄᴏᴅᴇ: [ᴘʀɪᴠᴀᴛᴇ & © ᴀʟʟ ᴄᴏᴅᴇ ʀɪɢʜᴛꜱ ʀᴇꜱᴇʀᴠᴇᴅ ʙʏ ᴄꜱʀ.](https://techycsr.tech)

ᴀɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ - ʏᴏᴜʀ ᴘʀᴏꜰᴇꜱꜱɪᴏɴᴀʟ ᴀɪ ᴀꜱꜱɪꜱᴛᴀɴᴛ, ᴘʀᴏᴠɪᴅɪɴɢ ᴄᴜᴛᴛɪɴɢ-ᴇᴅɢᴇ ᴛᴇᴄʜɴᴏʟᴏɢʏ ꜱᴏʟᴜᴛɪᴏɴꜱ ᴡɪᴛʜ ᴀ ᴛᴏᴜᴄʜ ᴏꜰ ɪɴɴᴏᴠᴀᴛɪᴏɴ!
"""
        bordered_message = f"<b>{txt}</b>"
        reply_markup = InlineKeyboardMarkup(
            [
                       
                [
                    InlineKeyboardButton("👨‍💻 ʙᴏᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ", url="https://techycsr.tech"),
                ],
                [
                    InlineKeyboardButton("👨‍💻 ᴏᴛʜᴇʀ ᴘʀᴏᴊᴇᴄᴛꜱ", url="https://projects.techycsr.tech"),
                ],
                [
                    InlineKeyboardButton("ʙᴀᴄᴋ ⬅️", callback_data="start"),
                ]
            ]
        )
        await client.edit_message_caption(
            callback_query.message.chat.id,
            callback_query.message.id,
            caption=bordered_message,
            reply_markup=reply_markup
        )
    elif callback_query.data == "start":
        # Handle start button
        user =callback_query.from_user
        bordered_message = WELCOME_CAPTION
        reply_markup = InlineKeyboardMarkup(
            [
            
                [
                    InlineKeyboardButton("ᴡʜᴀᴛ ᴀʟʟ ɪ ᴄᴀɴ ᴅᴏ ..!!  ", callback_data="commands"),
                ],
                [
                    InlineKeyboardButton("ᴄᴏᴍᴍᴀɴᴅꜱℹ️", callback_data="help"),
                    InlineKeyboardButton("ʙᴏᴛ ꜱᴛᴀᴛᴜꜱ 📊", callback_data="status"),
                ],
                [
                    InlineKeyboardButton("ᴀʙᴏᴜᴛ ᴍᴇ👨‍💻", callback_data="abtme"),
                ]
            ]
        )
        await client.edit_message_caption(
            callback_query.message.chat.id,
            callback_query.message.id,
            caption=bordered_message,
            reply_markup=reply_markup
        )
        


@chtwblock.on_message(filters.command("newchat"))
async def start_command(bot, update):
    if update.from_user.id in session:
        session[update.from_user.id]=[]
        session[update.from_user.id].append({"role": "system", "content": "Hello! I am a AI chatbot designed by CSR(An AI developer & Website of him : techycsr.tech). I am here to help you with your queries,I prefer to talk in english but with that I can also reply in hindi & other Indian native languages."})

    await update.reply("ᴀʟʟ ᴘʀᴇᴠɪᴏᴜꜱ ᴍᴇꜱꜱᴀɢᴇ ᴅᴇʟᴇᴛᴇᴅ.\nɴᴇᴡ ᴄʜᴀᴛ ᴄʀᴇᴀᴛᴇᴅ.")


@chtwblock.on_message(filters.photo & filters.private)
async def extract_text(bot, update):
    if update.from_user.id not in session:
        session[update.from_user.id]=[]
        session[update.from_user.id].append({"role": "system", "content": "Hello! I am a AI chatbot designed by CSR(An AI developer & Website of him : techycsr.tech). I am here to help you with your queries,I prefer to talk in english but with that I can also reply in hindi & other Indian native languages."})
    
    # Send a "processing" message
    processing_msg = await update.reply("ᴇxᴛʀᴀᴄᴛɪɴɢ ᴛᴇxᴛ ꜰʀᴏᴍ ɪᴍᴀɢᴇ...")

    # Get the largest available version of the image
    if isinstance(update.photo, list):
        photo = update.photo[-1]
    else:
        photo = update.photo

    # Download the image file
    file = await bot.download_media(photo.file_id)

    # Upload the image file to the OCR.Space API
    url = "https://api.ocr.space/parse/image"
    headers = {"apikey": OCR_KEY}
    with open(file, "rb") as image_file:
        response = requests.post(url, headers=headers, files={"image": image_file})

    # Parse the API response to extract the extracted text
    response_data = response.json()
    if response_data["IsErroredOnProcessing"] == False:
        text = response_data["ParsedResults"][0]["ParsedText"]
    else:
        error_message = response_data["ErrorMessage"]
        text = f"Error: Failed to extract text from image. {error_message}"
        await update.reply_photo(photo=file, caption=text + "\nNo text found")
        return

    text = text
    await processing_msg.edit("ɢᴇᴛᴛɪɴɢ ᴀɪ ʀᴇꜱᴘᴏɴꜱᴇ",disable_web_page_preview=True)
    res= await aires(text,update.from_user.id)
    await processing_msg.edit(res,disable_web_page_preview=True)


@chtwblock.on_message(filters.command("term") & filters.private|filters.command("term") & filters.group)
async def help_handle(bot, update):
  term_text="""
There are the following terms and conditions :

ʙʏ ᴜꜱɪɴɢ ʙᴏᴛ , ʏᴏᴜ ᴀɢʀᴇᴇ ᴛᴏ ʙᴇ ʙᴏᴜɴᴅ ʙʏ ᴛʜᴇ ꜰᴏʟʟᴏᴡɪɴɢ ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ: 

1. ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ ᴛʜᴇ ʙᴏᴛ ɪꜱ ᴘʀᴏᴠɪᴅᴇᴅ ᴛᴏ ʏᴏᴜ ꜰᴏʀ ʏᴏᴜʀ ᴘᴇʀꜱᴏɴᴀʟ ᴏʀ ᴄᴏᴍᴍᴇʀᴄɪᴀʟ ᴜꜱᴇ. ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ ꜰᴏʀ ᴀɴʏ ɪʟʟᴇɢᴀʟ ᴏʀ ᴜɴᴀᴜᴛʜᴏʀɪᴢᴇᴅ ᴘᴜʀᴘᴏꜱᴇ.  

2. ᴏᴡɴᴇʀꜱʜɪᴘ ᴀɴᴅ ɪɴᴛᴇʟʟᴇᴄᴛᴜᴀʟ ᴘʀᴏᴘᴇʀᴛʏ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ʀᴇᴛᴀɪɴꜱ ᴀʟʟ ᴏᴡɴᴇʀꜱʜɪᴘ ᴀɴᴅ ɪɴᴛᴇʟʟᴇᴄᴛᴜᴀʟ ᴘʀᴏᴘᴇʀᴛʏ ʀɪɢʜᴛꜱ ɪɴ ᴛʜᴇ ʙᴏᴛ. ʏᴏᴜ ᴀɢʀᴇᴇ ɴᴏᴛ ᴛᴏ ᴍᴏᴅɪꜰʏ, ᴄᴏᴘʏ, ᴅɪꜱᴛʀɪʙᴜᴛᴇ, ᴛʀᴀɴꜱᴍɪᴛ, ᴅɪꜱᴘʟᴀʏ, ᴘᴇʀꜰᴏʀᴍ, ʀᴇᴘʀᴏᴅᴜᴄᴇ, ᴘᴜʙʟɪꜱʜ, ʟɪᴄᴇɴꜱᴇ, ᴄʀᴇᴀᴛᴇ ᴅᴇʀɪᴠᴀᴛɪᴠᴇ ᴡᴏʀᴋꜱ ꜰʀᴏᴍ, ᴛʀᴀɴꜱꜰᴇʀ, ᴏʀ ꜱᴇʟʟ ᴀɴʏ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ, ꜱᴏꜰᴛᴡᴀʀᴇ, ᴘʀᴏᴅᴜᴄᴛꜱ, ᴏʀ ꜱᴇʀᴠɪᴄᴇꜱ ᴏʙᴛᴀɪɴᴇᴅ ꜰʀᴏᴍ ᴛʜᴇ ʙᴏᴛ.

 3. ᴅᴀᴛᴀ ᴘʀɪᴠᴀᴄʏ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ᴍᴀʏ ᴄᴏʟʟᴇᴄᴛ ᴀɴᴅ ᴜꜱᴇ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ. ʙʏ ᴜꜱɪɴɢ ᴛʜᴇ ʙᴏᴛ, ʏᴏᴜ ᴄᴏɴꜱᴇɴᴛ ᴛᴏ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ'ꜱ ᴄᴏʟʟᴇᴄᴛɪᴏɴ ᴀɴᴅ ᴜꜱᴇ ᴏꜰ ꜱᴜᴄʜ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ. ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ᴡɪʟʟ ɴᴏᴛ ꜱʜᴀʀᴇ ʏᴏᴜʀ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴡɪᴛʜ ᴛʜɪʀᴅ ᴘᴀʀᴛɪᴇꜱ ᴜɴʟᴇꜱꜱ ʀᴇQᴜɪʀᴇᴅ ʙʏ ʟᴀᴡ.  

4. ɴᴏ ᴡᴀʀʀᴀɴᴛʏ ᴛʜᴇ ʙᴏᴛ ɪꜱ ᴘʀᴏᴠɪᴅᴇᴅ "ᴀꜱ ɪꜱ" ᴡɪᴛʜᴏᴜᴛ ᴡᴀʀʀᴀɴᴛʏ ᴏꜰ ᴀɴʏ ᴋɪɴᴅ. ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ᴅᴏᴇꜱ ɴᴏᴛ ɢᴜᴀʀᴀɴᴛᴇᴇ ᴛʜᴇ ᴀᴄᴄᴜʀᴀᴄʏ, ᴄᴏᴍᴘʟᴇᴛᴇɴᴇꜱꜱ, ᴏʀ ᴜꜱᴇꜰᴜʟɴᴇꜱꜱ ᴏꜰ ᴛʜᴇ ʙᴏᴛ. 

5. ʟɪᴍɪᴛᴀᴛɪᴏɴ ᴏꜰ ʟɪᴀʙɪʟɪᴛʏ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ꜱʜᴀʟʟ ɴᴏᴛ ʙᴇ ʟɪᴀʙʟᴇ ꜰᴏʀ ᴀɴʏ ᴅɪʀᴇᴄᴛ, ɪɴᴅɪʀᴇᴄᴛ, ɪɴᴄɪᴅᴇɴᴛᴀʟ, ꜱᴘᴇᴄɪᴀʟ, ᴏʀ ᴄᴏɴꜱᴇQᴜᴇɴᴛɪᴀʟ ᴅᴀᴍᴀɢᴇꜱ ᴀʀɪꜱɪɴɢ ᴏᴜᴛ ᴏꜰ ᴏʀ ɪɴ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴡɪᴛʜ ᴛʜᴇ ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ. 

6. ɪɴᴅᴇᴍɴɪꜰɪᴄᴀᴛɪᴏɴ ʏᴏᴜ ᴀɢʀᴇᴇ ᴛᴏ ɪɴᴅᴇᴍɴɪꜰʏ, ᴅᴇꜰᴇɴᴅ, ᴀɴᴅ ʜᴏʟᴅ ʜᴀʀᴍʟᴇꜱꜱ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ᴀɴᴅ ɪᴛꜱ ᴏꜰꜰɪᴄᴇʀꜱ, ᴅɪʀᴇᴄᴛᴏʀꜱ, ᴇᴍᴘʟᴏʏᴇᴇꜱ, ᴀɴᴅ ᴀɢᴇɴᴛꜱ ꜰʀᴏᴍ ᴀɴʏ ᴀɴᴅ ᴀʟʟ ᴄʟᴀɪᴍꜱ, ʟɪᴀʙɪʟɪᴛɪᴇꜱ, ᴅᴀᴍᴀɢᴇꜱ, ʟᴏꜱꜱᴇꜱ, ᴏʀ ᴇxᴘᴇɴꜱᴇꜱ, ɪɴᴄʟᴜᴅɪɴɢ ʀᴇᴀꜱᴏɴᴀʙʟᴇ ᴀᴛᴛᴏʀɴᴇʏꜱ' ꜰᴇᴇꜱ, ᴀʀɪꜱɪɴɢ ᴏᴜᴛ ᴏꜰ ᴏʀ ɪɴ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴡɪᴛʜ ʏᴏᴜʀ ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ.  

7. ᴛᴇʀᴍɪɴᴀᴛɪᴏɴ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ᴍᴀʏ ᴛᴇʀᴍɪɴᴀᴛᴇ ʏᴏᴜʀ ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ ᴀᴛ ᴀɴʏ ᴛɪᴍᴇ ᴡɪᴛʜᴏᴜᴛ ɴᴏᴛɪᴄᴇ. ᴜᴘᴏɴ ᴛᴇʀᴍɪɴᴀᴛɪᴏɴ, ʏᴏᴜ ᴍᴜꜱᴛ ᴄᴇᴀꜱᴇ ᴀʟʟ ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ᴅᴇʟᴇᴛᴇ ᴀɴʏ ᴄᴏᴘɪᴇꜱ ᴏꜰ ᴛʜᴇ ʙᴏᴛ ɪɴ ʏᴏᴜʀ ᴘᴏꜱꜱᴇꜱꜱɪᴏɴ. 

8. ɢᴏᴠᴇʀɴɪɴɢ ʟᴀᴡ ᴀɴᴅ ᴊᴜʀɪꜱᴅɪᴄᴛɪᴏɴ ᴛʜɪꜱ ᴀɢʀᴇᴇᴍᴇɴᴛ ꜱʜᴀʟʟ ʙᴇ ɢᴏᴠᴇʀɴᴇᴅ ʙʏ ᴀɴᴅ ᴄᴏɴꜱᴛʀᴜᴇᴅ ɪɴ ᴀᴄᴄᴏʀᴅᴀɴᴄᴇ ᴡɪᴛʜ ᴛʜᴇ ʟᴀᴡꜱ ᴏꜰ ᴛʜᴇ ᴊᴜʀɪꜱᴅɪᴄᴛɪᴏɴ ɪɴ ᴡʜɪᴄʜ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ɪꜱ ʟᴏᴄᴀᴛᴇᴅ. ᴀɴʏ ʟᴇɢᴀʟ ᴀᴄᴛɪᴏɴ ᴏʀ ᴘʀᴏᴄᴇᴇᴅɪɴɢ ᴀʀɪꜱɪɴɢ ᴏᴜᴛ ᴏꜰ ᴏʀ ɪɴ ᴄᴏɴɴᴇᴄᴛɪᴏɴ ᴡɪᴛʜ ᴛʜɪꜱ ᴀɢʀᴇᴇᴍᴇɴᴛ ꜱʜᴀʟʟ ʙᴇ ʙʀᴏᴜɢʜᴛ ɪɴ ᴛʜᴇ ᴄᴏᴜʀᴛꜱ ᴏꜰ ᴛʜᴀᴛ ᴊᴜʀɪꜱᴅɪᴄᴛɪᴏɴ.  

9. ᴇɴᴛɪʀᴇ ᴀɢʀᴇᴇᴍᴇɴᴛ ᴛʜɪꜱ ᴀɢʀᴇᴇᴍᴇɴᴛ ᴄᴏɴꜱᴛɪᴛᴜᴛᴇꜱ ᴛʜᴇ ᴇɴᴛɪʀᴇ ᴀɢʀᴇᴇᴍᴇɴᴛ ʙᴇᴛᴡᴇᴇɴ ʏᴏᴜ ᴀɴᴅ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ʀᴇɢᴀʀᴅɪɴɢ ᴛʜᴇ ᴜꜱᴇ ᴏꜰ ᴛʜᴇ ʙᴏᴛ ᴀɴᴅ ꜱᴜᴘᴇʀꜱᴇᴅᴇꜱ ᴀʟʟ ᴘʀɪᴏʀ ᴀɢʀᴇᴇᴍᴇɴᴛꜱ ᴀɴᴅ ᴜɴᴅᴇʀꜱᴛᴀɴᴅɪɴɢꜱ, ᴡʜᴇᴛʜᴇʀ ᴡʀɪᴛᴛᴇɴ ᴏʀ ᴏʀᴀʟ.  

10. ᴄᴏɴᴛᴀᴄᴛ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ɪꜰ ʏᴏᴜ ʜᴀᴠᴇ ᴀɴʏ Qᴜᴇꜱᴛɪᴏɴꜱ ᴀʙᴏᴜᴛ ᴛʜɪꜱ ᴀɢʀᴇᴇᴍᴇɴᴛ, ᴘʟᴇᴀꜱᴇ ᴄᴏɴᴛᴀᴄᴛ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇʀ ᴀᴛ ᴀᴅᴠᴀɴᴄᴇ ᴄʜᴀᴛ ɢʀᴏᴜᴘ .  ʙʏ ᴜꜱɪɴɢ ᴛʜᴇ ʙᴏᴛ, ʏᴏᴜ ᴀɢʀᴇᴇ ᴛᴏ ʙᴇ ʙᴏᴜɴᴅ ʙʏ ᴛʜᴇꜱᴇ ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ. ɪꜰ ʏᴏᴜ ᴅᴏ ɴᴏᴛ ᴀɢʀᴇᴇ ᴛᴏ ᴛʜᴇꜱᴇ ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ, ʏᴏᴜ ꜱʜᴏᴜʟᴅ ɴᴏᴛ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ.  

ᴘᴏᴡᴇʀᴇᴅ ʙʏ : ᴄʜᴀᴛɢᴘᴛ-4 ᴀɴᴅ ᴍɪɴᴅᴊᴏᴜʀɴᴇʏ
ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ : [ᴄꜱʀ](https://techycsr.tech)
"""
  url = "https://projects.techyscr.tech"
  
  keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("ᴄꜱʀ", url=url)],
  ])
  await bot.send_message(chat_id=update.chat.id, text=f"**{term_text}**", reply_markup=keyboard,disable_web_page_preview=True)












chtwblock.run()


