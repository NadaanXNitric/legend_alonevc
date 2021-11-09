import asyncio

from pyrogram import Client, filters
from pyrogram.errors import UserAlreadyParticipant

from config import SUDO_USERS, ASSISTANT_NAME
from helpers.decorators import authorized_users_only, errors
from callsmusic import client as USER


@Client.on_message(filters.command(["play"]) & ~filters.private & ~filters.bot)
@authorized_users_only
@errors
async def addchannel(client, message):
    chid = message.chat.id
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>𝐀𝐝𝐝 𝐌𝐞 𝐀𝐬 𝐀𝐝𝐦𝐢𝐧 𝐅𝐢𝐫𝐬𝐭 𝐒𝐭𝐮𝐩𝐢𝐝.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "⟁⃤ { #𓆩𓆩𝐀𝐋𝐎𝐍𝐄𓆪𓆪 ོ MUSIC"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "𝐈 𝐉𝐨𝐢𝐧𝐞𝐝 𝐀𝐬 𝐑𝐞𝐪𝐮𝐞𝐬𝐭𝐞𝐝 𝐁𝐲 𝐘𝐨𝐮 ✌️")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐇𝐞𝐫𝐞...𝐔𝐬𝐞 𝐏𝐥𝐚𝐲 𝐂𝐨𝐦𝐦𝐚𝐧𝐝 𝐓𝐨 𝐏𝐥𝐚𝐲 𝐌𝐮𝐬𝐢𝐜.🎵</b>",
        )
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 𝐅𝐥𝐨𝐨𝐝 𝐄𝐫𝐫𝐨𝐫 🛑</b> \n\𝐇𝐞𝐲 {user.first_name},𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐉𝐨𝐢𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩. 𝐌𝐚𝐲 𝐁𝐞 𝐈𝐭𝐬 𝐁𝐚𝐧𝐧𝐞𝐝 𝐀𝐧𝐝 𝐀𝐧𝐲 𝐎𝐭𝐡𝐞𝐫 𝐈𝐬𝐬𝐮𝐞!</b>",
        )
        return
    await message.reply_text(
        "<b>𝐇𝐞𝐲 𝐌𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐉𝐨𝐢𝐧𝐞𝐝.. 𝐇𝐮𝐫𝐫𝐞𝐲 🐬🤞</b>",
    )


@USER.on_message(filters.group & filters.command(["userbotleave"]))
@authorized_users_only
async def rem(USER, message):
    try:
        await USER.leave_chat(message.chat.id)
    except:
        await message.reply_text(
            "<b> 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐋𝐞𝐚𝐯𝐞.. ."
            "\n\nOr 𝐈𝐟 𝐘𝐨𝐮 𝐖𝐚𝐧𝐭 𝐊𝐢𝐜𝐤 𝐇𝐢𝐦..🥺</b>",
        )
        return


@Client.on_message(filters.command(["userbotleaveall"]))
async def bye(client, message):
    if message.from_user.id in SUDO_USERS:
        left = 0
        failed = 0
        lol = await message.reply("Assistant Leaving all chats")
        async for dialog in USER.iter_dialogs():
            try:
                await USER.leave_chat(dialog.chat.id)
                left = left + 1
                await lol.edit(
                    f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
                )
            except:
                failed = failed + 1
                await lol.edit(
                    f"Assistant leaving... Left: {left} chats. Failed: {failed} chats."
                )
            await asyncio.sleep(0.7)
        await client.send_message(
            message.chat.id, f"Left {left} chats. Failed {failed} chats."
        )


@Client.on_message(
    filters.command(["play"]) & ~filters.private & ~filters.bot
)
@authorized_users_only
@errors
async def addcchannel(client, message):
    try:
        conchat = await client.get_chat(message.chat.id)
        conid = conchat.linked_chat.id
        chid = conid
    except:
        await message.reply("𝐈𝐬 𝐂𝐡𝐚𝐭 𝐈𝐬 𝐋𝐢𝐧𝐤𝐞𝐝.🧐")
        return
    try:
        invitelink = await client.export_chat_invite_link(chid)
    except:
        await message.reply_text(
            "<b>𝐀𝐝𝐝 𝐌𝐞 𝐀𝐬 𝐀𝐝𝐦𝐢𝐧 𝐅𝐢𝐫𝐬𝐭 𝐒𝐭𝐮𝐩𝐢𝐝.</b>",
        )
        return

    try:
        user = await USER.get_me()
    except:
        user.first_name = "⟁⃤ { #𓆩𓆩𝐀𝐋𝐎𝐍𝐄𓆪𓆪 ོ MUSIC"

    try:
        await USER.join_chat(invitelink)
        await USER.send_message(message.chat.id, "I joined here as you requested")
    except UserAlreadyParticipant:
        await message.reply_text(
            "<b>𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐀𝐥𝐫𝐞𝐚𝐝𝐲 𝐈𝐧 𝐭𝐡𝐢𝐬 𝐜𝐡𝐚𝐭..</b>",
        )
        return
    except Exception as e:
        print(e)
        await message.reply_text(
            f"<b>🛑 𝐅𝐥𝐨𝐨𝐝 𝐄𝐫𝐫𝐨𝐫 🛑</b> \n\𝐇𝐞𝐲 {user.first_name},𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐂𝐨𝐮𝐥𝐝𝐧'𝐭 𝐉𝐨𝐢𝐧 𝐘𝐨𝐮𝐫 𝐆𝐫𝐨𝐮𝐩. 𝐌𝐚𝐲 𝐁𝐞 𝐈𝐭𝐬 𝐁𝐚𝐧𝐧𝐞𝐝 𝐀𝐧𝐝 𝐀𝐧𝐲 𝐎𝐭𝐡𝐞𝐫 𝐈𝐬𝐬𝐮𝐞!</b>",
        )
        return
    await message.reply_text(
        "<b>𝐇𝐞𝐲 𝐌𝐲 𝐀𝐬𝐬𝐢𝐬𝐭𝐚𝐧𝐭 𝐈𝐬 𝐉𝐨𝐢𝐧𝐞𝐝.. 𝐇𝐮𝐫𝐫𝐞𝐲 🐬🤞</b>",
    )