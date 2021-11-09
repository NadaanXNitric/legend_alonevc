from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from config import BOT_NAME as bn
from helpers.filters import other_filters2


@Client.on_message(other_filters2)
async def start(_, message: Message):
    await message.reply_sticker("CAADBQADRQIAAhHHQFSfHJ-IR0eN6gI")
    await message.reply_text(
        f"""**- 𝐇𝐞𝐲 𝐀𝐦 {bn} 💛🐬,

- 𝐈 𝐂𝐚𝐧 𝐏𝐥𝐚𝐲 𝐌𝐮𝐬𝐢𝐜 𝐈𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩'𝐬 𝐕𝐨𝐢𝐜𝐞 𝐂𝐚𝐥𝐥. 𝐃𝐞𝐯𝐞𝐥𝐨𝐩𝐞𝐝 𝐁𝐲 [𝐌𝐀𝐇𝐈](https://t.me/ALONE_BOY_XD_01) ❣️🤞.

𝘼𝙙𝙙 𝙢𝙚 𝙩𝙤 𝙮𝙤𝙪𝙧 𝙜𝙧𝙤𝙪𝙥 𝙖𝙣𝙙 𝙥𝙡𝙖𝙮 𝙢𝙪𝙨𝙞𝙘 𝙛𝙧𝙚𝙚𝙡𝙮 😘💕**
        """,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                         " 𝐎𝐰𝐧𝐞𝐫 ", url="https://t.me/ALONE_BOY_XD_01")
                  ],[
                    InlineKeyboardButton(
                        "😈 𝐒𝐮𝐩𝐩𝐨𝐫𝐭", url="https://t.me/shivamdemon"
                    ),
                    InlineKeyboardButton(
                        "✌️ 𝐅𝐫𝐢𝐞𝐧𝐝", url="https://t.me/crowrace"
                    )
                ],[ 
                    InlineKeyboardButton(
                        "➕ 𝐀𝐝𝐝 𝐓𝐨 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩 ➕", url="https://t.me/LEGEND_ALONE_MUSIC_BOT?startgroup=true"
                    )]
            ]
        ),
     disable_web_page_preview=True
    )

@Client.on_message(filters.command("start") & ~filters.private & ~filters.channel)
async def gstart(_, message: Message):
      await message.reply_text("""** 𝐀𝐥𝐨𝐧𝐞 𝐌𝐮𝐬𝐢𝐜 𝐏𝐥𝐚𝐲𝐞𝐫 𝐈𝐬 𝐎𝐧𝐥𝐢𝐧𝐞 ✅**""",
      reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "🔊 𝐌𝐚𝐧𝐚𝐠𝐞𝐫", url="https://t.me/ALONE_BOY_XD_01")
                ]
            ]
        )
   )

