import os
from os import path
from typing import Callable
from pyrogram import Client, filters
from pyrogram.types import Message, Voice, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserAlreadyParticipant
from Client import callsmusic, queues
from Client.callsmusic import client as USER
from helpers.admins import get_administrators
import requests
import aiohttp
import yt_dlp
from youtube_search import YoutubeSearch
import converter
from youtube import youtube
from config import DURATION_LIMIT, que, SUDO_USERS
from cache.admins import admins as a
from helpers.filters import command
from helpers.decorators import errors, authorized_users_only
from helpers.errors import DurationLimitError
from helpers.gets import get_url, get_file_name
from helpers.channelmusic import get_chat_id
import aiofiles
import ffmpeg
from PIL import Image, ImageFont, ImageDraw
from pytgcalls.types.input_stream import InputAudioStream


def transcode(filename):
    ffmpeg.input(filename).output("input.raw", format='s16le', acodec='pcm_s16le', ac=2, ar='48k').overwrite_output().run() 
    os.remove(filename)

# Convert seconds to mm:ss
def convert_seconds(seconds):
    seconds = seconds % (24 * 3600)
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return "%02d:%02d" % (minutes, seconds)


# Convert hh:mm:ss to seconds
def time_to_seconds(time):
    stringt = str(time)
    return sum(int(x) * 60 ** i for i, x in enumerate(reversed(stringt.split(':'))))


# Change image size
def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def generate_cover(requested_by, title, views, duration, thumbnail):
    async with aiohttp.ClientSession() as session:
        async with session.get(thumbnail) as resp:
            if resp.status == 200:
                f = await aiofiles.open("background.png", mode="wb")
                await f.write(await resp.read())
                await f.close()

    image1 = Image.open("./background.png")
    image2 = Image.open("etc/foreground.png")
    image3 = changeImageSize(1280, 720, image1)
    image4 = changeImageSize(1280, 720, image2)
    image5 = image3.convert("RGBA")
    image6 = image4.convert("RGBA")
    Image.alpha_composite(image5, image6).save("temp.png")
    img = Image.open("temp.png")
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("etc/font.otf", 32)
    draw.text((190, 550), f"Title: {title}", (255, 255, 255), font=font)
    draw.text(
        (190, 590), f"Duration: {duration}", (255, 255, 255), font=font
    )
    draw.text((190, 630), f"Views: {views}", (255, 255, 255), font=font)
    draw.text((190, 670),
        f"Added By: {requested_by}",
        (255, 255, 255),
        font=font,
    )
    img.save("final.png")
    os.remove("temp.png")
    os.remove("background.png")




@Client.on_message(command("play") 
                   & filters.group
                   & ~filters.edited 
                   & ~filters.forwarded
                   & ~filters.via_bot)
async def play(_, message: Message):

    lel = await message.reply("🔄 **𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠 𝐘𝐨𝐮𝐫 𝐒𝐨𝐧𝐠...**")
    
    administrators = await get_administrators(message.chat)
    chid = message.chat.id

    try:
        user = await USER.get_me()
    except:
        user.first_name = " {user.first_name}"
    usar = user
    wew = usar.id
    try:
        await _.get_chat_member(chid, wew)
    except:
        for administrator in administrators:
            if administrator == message.from_user.id:
                try:
                    invitelink = await _.export_chat_invite_link(chid)
                except:
                    await lel.edit(
                        "<b>𝐀𝐝𝐝 𝐌𝐞 𝐀𝐬 𝐀𝐝𝐦𝐢𝐧 𝐅𝐢𝐫𝐬𝐭 𝐒𝐭𝐮𝐩𝐢𝐝.</b>")
                    return

                try:
                    await USER.join_chat(invitelink)
                    await USER.send_message(
                        message.chat.id, "**𝐇𝐞𝐲 𝐌𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐉𝐨𝐢𝐧𝐞𝐝.. 𝐇𝐮𝐫𝐫𝐞𝐲 🐬🤞**")

                except UserAlreadyParticipant:
                    pass
                except Exception:
                    await lel.edit(
                        f"<b>🛑 𝐅𝐥𝐨𝐨𝐝 𝐄𝐫𝐫𝐨𝐫 🛑</b> \n\𝐇𝐞𝐲 {user.first_name},𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐉𝐨𝐢𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩. 𝐌𝐚𝐲 𝐁𝐞 𝐈𝐭𝐬 𝐁𝐚𝐧𝐧𝐞𝐝 𝐀𝐧𝐝 𝐀𝐧𝐲 𝐎𝐭𝐡𝐞𝐫 𝐈𝐬𝐬𝐮𝐞!")
    try:
        await USER.get_chat(chid)
    except:
        await lel.edit(
            f"<i>𝐇𝐞𝐲 {user.first_name}, 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐍𝐨𝐭 𝐇𝐞𝐫𝐞 , 𝐒𝐞𝐧𝐝 /play 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐅𝐢𝐫𝐬𝐭 𝐓𝐨 𝐀𝐝𝐝 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭.</i>")
        return
    
    audio = (message.reply_to_message.audio or message.reply_to_message.voice) if message.reply_to_message else None
    url = get_url(message)

    if audio:
        if round(audio.duration / 60) > DURATION_LIMIT:
            raise DurationLimitError(
                f"❌ 𝐕𝐢𝐝𝐞𝐨 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬."
            )

        file_name = get_file_name(audio)
        title = file_name
        thumb_name = "https://telegra.ph/file/5b2ed5398e7cc024c8838.jpg"
        thumbnail = thumb_name
        duration = round(audio.duration / 60)
        views = "Locally added"

        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="𝐒𝐮𝐩𝐩𝐨𝐫𝐭🔊",
                        url="https://t.me/alone_boy_xd_01")
                   
                ]
            ]
        )
        
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(
            (await message.reply_to_message.download(file_name))
            if not path.isfile(path.join("downloads", file_name)) else file_name
        )

    elif url:
        try:
            results = YoutubeSearch(url, max_results=1).to_dict()
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")
            
            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝐘𝐨𝐮𝐭𝐮𝐛𝐞 🎬",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 📥",
                            url=f"{durl}")

                    ]
                ]
            )
        except Exception as e:
            title = "NaN"
            thumb_name = "https://telegra.ph/file/5b2ed5398e7cc024c8838.jpg"
            duration = "NaN"
            views = "NaN"
            keyboard = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="𝐘𝐨𝐮𝐭𝐮𝐛𝐞 🎬",
                                url=f"https://youtube.com")

                        ]
                    ]
                )
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐕𝐢𝐝𝐞𝐨 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)     
        file_path = await converter.convert(youtube.download(url))
    else:
        if len(message.command) < 2:
            return await lel.edit("🧐 **𝐖𝐡𝐢𝐜𝐡 𝐒𝐨𝐧𝐠 𝐘𝐨𝐮 𝐖𝐚𝐧𝐧𝐚 𝐏𝐥𝐚𝐲 ??**")
        await lel.edit("🔎 **𝐅𝐢𝐧𝐝𝐢𝐧𝐠...𝐇𝐨𝐥𝐝 𝐎𝐧**")
        query = message.text.split(None, 1)[1]
        # print(query)
        await lel.edit("🎵 **𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠...𝐇𝐨𝐥𝐝 𝐎𝐧**")
        try:
            results = YoutubeSearch(query, max_results=1).to_dict()
            url = f"https://youtube.com{results[0]['url_suffix']}"
            # print results
            title = results[0]["title"]       
            thumbnail = results[0]["thumbnails"][0]
            thumb_name = f'thumb{title}.jpg'
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumb_name, 'wb').write(thumb.content)
            duration = results[0]["duration"]
            url_suffix = results[0]["url_suffix"]
            views = results[0]["views"]
            durl = url
            durl = durl.replace("youtube", "youtubepp")

            secmul, dur, dur_arr = 1, 0, duration.split(':')
            for i in range(len(dur_arr)-1, -1, -1):
                dur += (int(dur_arr[i]) * secmul)
                secmul *= 60
                
        except Exception as e:
            await lel.edit(
                "❌ 𝐒𝐨𝐫𝐫𝐲 𝐒𝐨𝐧𝐠 𝐍𝐨𝐭 𝐅𝐢𝐧𝐝 ☹ ️𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧..."
            )
            print(str(e))
            return

        keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="𝐘𝐨𝐮𝐭𝐮𝐛𝐞 🎬",
                            url=f"{url}"),
                        InlineKeyboardButton(
                            text="𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝 📥",
                            url=f"{durl}")

                    ]
                ]
            )
        
        if (dur / 60) > DURATION_LIMIT:
             await lel.edit(f"❌ 𝐕𝐢𝐝𝐞𝐨 𝐈𝐬 𝐋𝐨𝐧𝐠𝐞𝐫 𝐓𝐡𝐚𝐧 {DURATION_LIMIT} 𝐌𝐢𝐧𝐮𝐭𝐞𝐬.")
             return
        requested_by = message.from_user.first_name
        await generate_cover(requested_by, title, views, duration, thumbnail)  
        file_path = await converter.convert(youtube.download(url))
    ACTV_CALLS = []
    for x in callsmusic.pytgcalls.active_calls:
       ACTV_CALLS.append(int(x.chat_id))
    if int(message.chat.id) in ACTV_CALLS:
        position = await queues.put(message.chat.id, file=file_path)
        await message.reply_photo(
        photo="final.png", 
        caption="**🎵 𝐒𝐨𝐧𝐠:** {}\n**🕒 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** {} 𝐦𝐢𝐧\n**👤 𝐀𝐝𝐝𝐞𝐝 𝐁𝐲:** {}\n\n**#⃣ 𝐐𝐮𝐞𝐮𝐞𝐝 𝐏𝐨𝐬𝐢𝐭𝐢𝐨𝐧:** {}".format(
        title, duration, message.from_user.mention(), position
        ),
        reply_markup=keyboard)
        os.remove("final.png")
        return await lel.delete()
    else:
        await callsmusic.pytgcalls.join_group_call(message.chat.id, file_path)
        await message.reply_photo(
        photo="final.png",
        reply_markup=keyboard,
        caption="**🎵 𝐒𝐨𝐧𝐠:** {}\n**🕒 𝐃𝐮𝐫𝐚𝐭𝐢𝐨𝐧:** {} 𝐦𝐢𝐧\n**👤 𝐀𝐝𝐝𝐞𝐝 𝐁𝐲:** {}\n\n**▶️ 𝐍𝐨𝐰 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐀𝐭 `{}`...**".format(
        title, duration, message.from_user.mention(), message.chat.title
        ), )
        os.remove("final.png")
        return await lel.delete()
