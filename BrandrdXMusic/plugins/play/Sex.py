from pyrogram import filters
import requests, random
from bs4 import BeautifulSoup
from BrandrdXMusic import app
import os, yt_dlp 
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

vdo_link = {}

keyboard = InlineKeyboardMarkup([
    [
        InlineKeyboardButton("⊝ ᴄʟᴏsᴇ ⊝", callback_data="close_data"), 
        InlineKeyboardButton("⊝ ᴠᴘʟᴀʏ⊝", callback_data="play"),
    ]
])

@app.on_callback_query(filters.regex("^play"))
async def play_callback(_, query):
    await play_video(query.from_user.id)  
    await query.answer("Playback started!")
        
@app.on_callback_query(filters.regex("^close_data"))
async def close_callback(_, query):
    await query.message.delete()

async def get_video_stream(link):
    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "downloads/%(id)s.%(ext)s",
        "geo_bypass": True,
        "nocheckcertificate": True,
        "quiet": True,
        "no_warnings": True,
    }
    x = yt_dlp.YoutubeDL(ydl_opts)
    info = x.extract_info(link, False)
    video = os.path.join("downloads", f"{info['id']}.{info['ext']}")
    if os.path.exists(video):
        return video
    x.download([link])
    return video

def get_video_info(title):
    url_base = f'https://xhamster.com/search/{title}'  # Updated URL
    try:
        with requests.Session() as s:
            r = s.get(url_base)
            soup = BeautifulSoup(r.text, "html.parser")
            video_list = soup.findAll('div', attrs={'class': 'thumb-block'})
            if video_list:
                random_video = random.choice(video_list)
                thumbnail = random_video.find('div', class_="thumb").find('img').get("src")
                if thumbnail:
                    thumbnail_500 = thumbnail.replace('/h', '/m').replace('/1.jpg', '/3.jpg')
                    link = random_video.find('div', class_="thumb-under").find('a').get("href")
                    if link and 'https://' not in link:
                        return {'link': 'https://xhamster.com' + link, 'thumbnail': thumbnail_500}
    except Exception as e:
        print(f"Error: {e}")
    return None

@app.on_message(filters.command("sex"))  # Added /sex command
async def get_random_video_info(client, message):
    await handle_video_request(client, message, "sex")

async def handle_video_request(client, message, command):
    if len(message.command) == 1:
        await message.reply("Please provide a title to search.")
        return

    title = ' '.join(message.command[1:])
    video_info = get_video_info(title)

    if video_info:
        video_link = video_info['link']
        video = await get_video_stream(video_link)

        if command == "sex":  # Updated to include "sex"
            vdo_link[message.chat.id] = {'link': video_link}
            keyboard1 = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("⊝ ᴄʟᴏsᴇ ⊝", callback_data="close_data"), 
                    InlineKeyboardButton("⊝ ᴠᴘʟᴀʏ⊝", callback_data="vplay"),
                ]
            ])
            await message.reply_video(video, caption=f"{title}", reply_markup=keyboard1)
    else:
        await message.reply(f"No video link found for '{title}'.")

def get_views_from_api(video_link):
    # Replace with actual logic to get views
    return "N/A"

def get_ratings_from_api(video_link):
    # Replace with actual logic to get ratings
    return "N/A"
