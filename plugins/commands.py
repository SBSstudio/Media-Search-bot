import os
import logging
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import START_MSG, CHANNELS, ADMINS, AUTH_CHANNEL, CUSTOM_FILE_CAPTION
from utils import Media, get_file_details
from pyrogram.errors import UserNotParticipant
logger = logging.getLogger(__name__)

HELP_TEXT = """
<b>My K-Drama Bot Help!</b> 

Click  Then type drama name &get results.

Or, 

Sned K-Drama Nme directly & get results.

Now My K-Drama Bot is allow Groups. Tap <b>Group Help 👥</b> Button & get more informations.

/request command for Request dramas. 

<b>Invite Friends & support us.</b>

Powered By @SBS_Studio
"""

@Client.on_message(filters.command("start"))
async def start(bot, cmd):
    usr_cmdall1 = cmd.text
    if usr_cmdall1.startswith("/start subinps"):
        if AUTH_CHANNEL:
            invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
            try:
                user = await bot.get_chat_member(int(AUTH_CHANNEL), cmd.from_user.id)
                if user.status == "kicked":
                    await bot.send_message(
                        chat_id=cmd.from_user.id,
                        text="Sorry Sir, You are Banned to use me.",
                        parse_mode="markdown",
                        disable_web_page_preview=True
                    )
                    return
            except UserNotParticipant:
                ident, file_id = cmd.text.split("_-_-_-_")
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="**Please Join My Updates Channel to use this Bot!**",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                            ],
                            [
                                InlineKeyboardButton(" 🔄 Try Again", callback_data=f"checksub#{file_id}")
                            ]
                        ]
                    ),
                    parse_mode="markdown"
                )
                return
            except Exception:
                await bot.send_message(
                    chat_id=cmd.from_user.id,
                    text="Something went Wrong.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        try:
            ident, file_id = cmd.text.split("_-_-_-_")
            filedetails = await get_file_details(file_id)
            for files in filedetails:
                title = files.file_name
                size=files.file_size
                f_caption=files.caption
                if CUSTOM_FILE_CAPTION:
                    try:
                        f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
                    except Exception as e:
                        print(e)
                        f_caption=f_caption
                if f_caption is None:
                    f_caption = f"{files.file_name}"
                buttons = [
                    [
                        InlineKeyboardButton('Search again', switch_inline_query_current_chat=''),
                        InlineKeyboardButton('More Bots', url='https://t.me/subin_works/122')
                    ]
                    ]
                await bot.send_cached_media(
                    chat_id=cmd.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        except Exception as err:
            await cmd.reply_text(f"Something went wrong!\n\n**Error:** `{err}`")
    elif len(cmd.command) > 1 and cmd.command[1] == 'subscribe':
        invite_link = await bot.create_chat_invite_link(int(AUTH_CHANNEL))
        await bot.send_message(
            chat_id=cmd.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                    ]
                ]
            )
        )
    else:
        await cmd.reply_text(
            START_MSG,
            parse_mode="Markdown",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('Search Hear 🔎', switch_inline_query_current_chat=''),
                        InlineKeyboardButton('Go Inline 🔅', switch_inline_query=''),
                    ],
                    [
                        InlineKeyboardButton("Help 🆘", callback_data="help"),
                    ],
                    [
                        InlineKeyboardButton('Updates Channel 🗣', url='https://t.me/SBS_Studio'),
                        InlineKeyboardButton("Invite Friends 👫", url="https://t.me/share/url?url=Hello%20People%F0%9F%98%8A%0A%0AAre%20you%20want%20to%20download%20more%20k-dramas%E2%9D%93%0A%0A%E2%80%A2%40myKdrama_bot%20will%20help%20you%20to%20Download%20k-dreams%20Easily%20.%0A%0AFeatures%20of%20%40myKdrama_bot%0A%20%20%20~%20Inline%20keyboard%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%20Request%20Dramas%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%20Inline%20Search%20Mode%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%2024%2A7%20Service%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%20Now%20Bot%20stable%20100%25%0A%0A12%20000%2B%20episodes%20were%20available%20on%20%40myKdrama_bot%0A%0ABot%20Link%3A-%20%20%40myKdrama_bot%0A%0A%7C%20Share%20Friends%20%26%20Support%20Us%20.%20.%20.%E2%9D%A4%EF%B8%8F"),
                    ],
                ]
            )
        )


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('total') & filters.user(ADMINS))
async def total(bot, message):
    """Show total files in database"""
    msg = await message.reply("Processing...⏳", quote=True)
    try:
        total = await Media.count_documents()
        await msg.edit(f'📁 Saved files: {total}')
    except Exception as e:
        logger.exception('Failed to check total files')
        await msg.edit(f'Error: {e}')


@Client.on_message(filters.command('logger') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))


@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return

    result = await Media.collection.delete_one({
        'file_name': media.file_name,
        'file_size': media.file_size,
        'mime_type': media.mime_type
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        await msg.edit('File not found in database')
@Client.on_message(filters.command('help'))
async def bot_info(bot, message):
    buttons = [
             [
                InlineKeyboardButton('About 📄', callback_data='about'),
                InlineKeyboardButton('Group Help 👥', callback_data='ghelp'),
             ],
            [
                InlineKeyboardButton('Home 🏠', callback_data='home'),
            ],
            ]
    await message.reply(text=HELP_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)
