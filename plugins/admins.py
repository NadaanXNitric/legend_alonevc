from asyncio.queues import QueueEmpty
from config import que
from pyrogram import Client, filters
from pyrogram.types import Message
import sira
import DeCalls
from cache.admins import set
from helpers.decorators import authorized_users_only, errors
from helpers.channelmusic import get_chat_id
from helpers.filters import command, other_filters
from Client import callsmusic
from pytgcalls.types.input_stream import InputAudioStream


@Client.on_message(command(["pause", "jeda"]) & other_filters)
@errors
@authorized_users_only
async def pause(_, message: Message):
    await callsmusic.pytgcalls.pause_stream(message.chat.id)
    await message.reply_sticker("CAACAgUAAx0CXmiEIwABAo5SYYny4TEOaOtHM2iAQYcXpopYKQcAAl8EAAKtOVFU4t6DLNYe1zseBA"
    )


@Client.on_message(command(["resume", "lanjut"]) & other_filters)
@errors
@authorized_users_only
async def resume(_, message: Message):
    await callsmusic.pytgcalls.resume_stream(message.chat.id)
    await message.reply_sticker("CAACAgUAAx0CXmiEIwABAo5UYYnz8nckQPJ2yr4ViMz8zPMI6jYAAmcEAAKtOVFUuXZntUPE9z4eBA"
    )


@Client.on_message(command(["end", "stop"]) & other_filters)
@errors
@authorized_users_only
async def stop(_, message: Message):
    try:
        callsmusic.queues.clear(message.chat.id)
    except QueueEmpty:
        pass

    await callsmusic.pytgcalls.leave_group_call(message.chat.id)
    await message.reply_sticker("CAACAgUAAx0CXmiEIwABAo5TYYn2KV6RA4JbhVsTMwHCENohYY4AAmYEAAKtOVFUDoN9ihMa9EceBA"
    )


@Client.on_message(command(["skip", "next"]) & other_filters)
@errors
@authorized_users_only
async def skip(_, message: Message):
    global que
    chat_id = message.chat.id
    ACTV_CALL = []
    for x in callsmusic.pytgcalls.active_calls:
        ACTV_CALL.append(int(x.chat_id))
    if int(chat_id) not in ACTV_CALL:
        await message.reply_text("❗ 𝐍𝐨𝐭𝐡𝐢𝐧𝐠 𝐈𝐬 𝐏𝐥𝐚𝐲𝐢𝐧𝐠 𝐓𝐨 𝐒𝐤𝐢𝐩")
    else:
        callsmusic.queues.task_done(chat_id)

        if callsmusic.queues.is_empty(chat_id):
            await callsmusic.pytgcalls.leave_group_call(chat_id)
        else:
            await callsmusic.pytgcalls.change_stream(
                chat_id, InputAudioStream(callsmusic.queues.get(chat_id)["file"])
            )

    qeue = que.get(chat_id)
    if qeue:
        skip = qeue.pop(0)
    if not qeue:
        return
    await message.reply_sticker("CAACAgUAAx0CXmiEIwABAo5VYYn2nS179FTt_lsmGe3xSjxVCQEAAmgEAAKtOVFUmF3LAtytI4YeBA"
   ) 


@Client.on_message(filters.command(["reload", "refresh"]))
@errors
@authorized_users_only
async def admincache(client, message: Message):
    set(
        message.chat.id,
        (
            member.user
            for member in await message.chat.get_members(filter="administrators")
        ),
    )

    await message.reply_sticker("CAACAgUAAx0CXmiEIwABAo5WYYn2y87cTguuxQtp9ikBsIVoTfwAAmwEAAKtOVFUZ754KHVWtOAeBA"
    )
