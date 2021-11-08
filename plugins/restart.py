from plugins import check_heroku
from helpers.filters import command
from pyrogram import Client, filters
from pyrogram import Client, filters
from helpers.decorators import sudo_users_only
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, Chat, CallbackQuery


@Client.on_message(command(["restart", "reboot"]) & ~filters.edited)
@sudo_users_only
@check_heroku
async def gib_restart(client, message, hap):
    msg_ = await message.reply_photo(
                                     photo="https://telegra.ph/file/52a737c84aa6ea1f3fbdc.jpg", 
                                     caption="**𝐑𝐞𝐬𝐭𝐚𝐫𝐭𝐢𝐧𝐠**\n**𝐏𝐥𝐞𝐚𝐬𝐞 𝐖𝐚𝐢𝐭🥺...**"
   )
    hap.restart()
