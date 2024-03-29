import os
import requests
import aiohttp
import yt_dlp

from pyrogram import Client, filters
from youtube_search import YoutubeSearch
from helpers.errors import capture_err
from config import BOT_USERNAME


@Client.on_message(filters.command("song") & ~filters.edited)
async def song(client, message):
    cap = "@warbotz"
    url = message.text.split(None, 1)[1]
    rkp = await message.reply("𝐏𝐫𝐨𝐜𝐞𝐬𝐬𝐢𝐧𝐠...𝐇𝐨𝐥𝐝 𝐎𝐧")
    if not url:
        await rkp.edit("**𝐖𝐡𝐢𝐜𝐡 𝐒𝐨𝐧𝐠 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭?**\n𝐔𝐬𝐚𝐠𝐞`/song <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except BaseException:
        return await rkp.edit("𝐅𝐚𝐢𝐥𝐞𝐝 𝐓𝐨 𝐅𝐢𝐧𝐝 𝐓𝐡𝐚𝐭 𝐒𝐨𝐧𝐠.")
    type = "audio"
    if type == "audio":
        opts = {
            "format": "bestaudio",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "writethumbnail": True,
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "320",
                }
            ],
            "outtmpl": "%(id)s.mp3",
            "quiet": True,
            "logtostderr": False,
        }
        song = True
    try:
        await rkp.edit("𝐃𝐨𝐰𝐧𝐥𝐨𝐚𝐝𝐢𝐧𝐠...𝐇𝐨𝐥𝐝 𝐎𝐧")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    time.time()
    if song:
        await rkp.edit("𝐔𝐩𝐥𝐨𝐚𝐝𝐢𝐧𝐠...𝐇𝐨𝐥𝐝 𝐎𝐧") #blaze
        lol = "./etc/thumb.jpg"
        lel = await message.reply_audio(
                 f"{rip_data['id']}.mp3",
                 duration=int(rip_data["duration"]),
                 title=str(rip_data["title"]),
                 performer=str(rip_data["uploader"]),
                 thumb=lol,
                 caption=cap)  #JEcode
        await rkp.delete()