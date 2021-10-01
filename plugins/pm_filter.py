from info import AUTH_CHANNEL, AUTH_USERS,  API_KEY, AUTH_GROUPS
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram import Client, filters
import re
from pyrogram.errors import UserNotParticipant
from utils import get_filter_results, get_file_details, is_subscribed, get_poster
BUTTONS = {}
BOT = {}
CUSTOM_FILE_CAPTION = """
💎Upload From:- @myKdrama_bot

〽️**Mixed English Subtitles**〽️

Thanks for using me ❤️ ©@SBS_Studio
"""
ABOUT_TEXT = """
- 🤖**Bot :** `My K-Drama Bot`
- 👨‍💻**Creator :** [This person](https://telegram.me/SBS_Studio)
- 🗣**Channel :** [SBS_Studio](https://telegram.me/SBS_Studio)
- 💻**Language :** [Python3](https://python.org)
- 📈**Library :** [Pyrogram](https://pyrogram.org)
- 💠**Server :** [Qovery](https://qovery.com)

🤖 Bot Updated on : `01-10-2021 | 13:24:04`
"""

HELP_TEXT = """
<b>My K-Drama Bot Help!</b> 

Click  Then type drama name &get results.

Or, 

Sned K-Drama Nme directly & get results.

Now My K-Drama Bot is allow Groups. Tap Group Help 👥 Button & get more informations.

/request command for Request dramas. 

<b>Invite Friends & support us.</b>

Powered By @SBS_Studio
"""

HOME_TEXT = """
Hello !<b>I'm My K-Drama Bot.</b>

Here you can search Koren Tv series in inline mode. You can start the search by pressing the buttons below or sending the K-Drama name 

Tap <b>Help 🆘</b> To get more informations.Tap /request To Request Drama.

Powered By @SBS_Studio
"""

GHELP_TEXT = """
<b>My K-Drama Bot Group Help!</b> 

Step 1: Click ➕ Add me On your Group ➕ Button & add me on your Group. 

Step 2: Make Admin on your group 

Finally Bot is work on your group.

Powered By @SBS_Studio
"""

@Client.on_message(filters.text & filters.private & filters.incoming & filters.user(AUTH_USERS) if AUTH_USERS else filters.text & filters.private & filters.incoming)
async def filter(client, message):
    if message.text.startswith("/"):
        return
    if AUTH_CHANNEL:
        invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        try:
            user = await client.get_chat_member(int(AUTH_CHANNEL), message.from_user.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.from_user.id,
                    text="Sorry Sir, You are Banned to use me.",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.from_user.id,
                text="**Please Join My Updates Channel to use this Bot!**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🤖 Join Updates Channel", url=invite_link.invite_link)
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.from_user.id,
                text="Something went Wrong.",
                parse_mode="markdown",
                disable_web_page_preview=True
            )
            return
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 100:    
        btn = []
        search = message.text
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}",callback_data=f"subinps#{file_id}")]
                    )
        else:
            await client.send_sticker(chat_id=message.from_user.id, sticker='CAACAgIAAxkBAAJFJ2FWtmf_-6YHXPCViJ2pSjqIUMPzAAJPAAMkcWIaWMzn4qdTlUgeBA')
            return

        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))

            else:
                await message.reply_text(f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="Next ▶",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_message(filters.text & filters.group & filters.incoming & filters.chat(AUTH_GROUPS) if AUTH_GROUPS else filters.text & filters.group & filters.incoming)
async def group(client, message):
    if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
        return
    if 2 < len(message.text) < 50:    
        btn = []
        search = message.text
        nyva=BOT.get("username")
        if not nyva:
            botusername=await client.get_me()
            nyva=botusername.username
            BOT["username"]=nyva
        files = await get_filter_results(query=search)
        if files:
            for file in files:
                file_id = file.file_id
                filename = f"[{get_size(file.file_size)}] {file.file_name}"
                btn.append(
                    [InlineKeyboardButton(text=f"{filename}", url=f"https://telegram.dog/{nyva}?start=subinps_-_-_-_{file_id}")]
                )
        else:
            return
        if not btn:
            return

        if len(btn) > 10: 
            btns = list(split_list(btn, 10)) 
            keyword = f"{message.chat.id}-{message.message_id}"
            BUTTONS[keyword] = {
                "total" : len(btns),
                "buttons" : btns
            }
        else:
            buttons = btn
            buttons.append(
                [InlineKeyboardButton(text="📃 Pages 1/1",callback_data="pages")]
            )
            poster=None
            if API_KEY:
                poster=await get_poster(search)
            if poster:
                await message.reply_photo(photo=poster, caption=f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))
            else:
                await message.reply_text(f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))
            return

        data = BUTTONS[keyword]
        buttons = data['buttons'][0].copy()

        buttons.append(
            [InlineKeyboardButton(text="Next ▶",callback_data=f"next_0_{keyword}")]
        )    
        buttons.append(
            [InlineKeyboardButton(text=f"📃 Pages 1/{data['total']}",callback_data="pages")]
        )
        poster=None
        if API_KEY:
            poster=await get_poster(search)
        if poster:
            await message.reply_photo(photo=poster, caption=f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(f"<b>Results for:</b> <i>{search} ‌‌‌‌‎ ­  ­  ­  ­  ­  </i>", reply_markup=InlineKeyboardMarkup(buttons))

    
def get_size(size):
    """Get size in readable format"""

    units = ["Bytes", "KB", "MB", "GB", "TB", "PB", "EB"]
    size = float(size)
    i = 0
    while size >= 1024.0 and i < len(units):
        i += 1
        size /= 1024.0
    return "%.2f %s" % (size, units[i])

def split_list(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]          



@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    clicked = query.from_user.id
    try:
        typed = query.message.reply_to_message.from_user.id
    except:
        typed = query.from_user.id
        pass
    if (clicked == typed):

        if query.data.startswith("next"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == int(data["total"]) - 2:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("◀ Back", callback_data=f"back_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📂 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
            else:
                buttons = data['buttons'][int(index)+1].copy()

                buttons.append(
                    [InlineKeyboardButton("◀ Back", callback_data=f"back_{int(index)+1}_{keyword}"),InlineKeyboardButton("Next ▶", callback_data=f"next_{int(index)+1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📂 Pages {int(index)+2}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return


        elif query.data.startswith("back"):
            ident, index, keyword = query.data.split("_")
            try:
                data = BUTTONS[keyword]
            except KeyError:
                await query.answer("You are using this for one of my old message, please send the request again.",show_alert=True)
                return

            if int(index) == 1:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("Next ▶", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📂 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return   
            else:
                buttons = data['buttons'][int(index)-1].copy()

                buttons.append(
                    [InlineKeyboardButton("◀ Back", callback_data=f"back_{int(index)-1}_{keyword}"),InlineKeyboardButton("Next ▶", callback_data=f"next_{int(index)-1}_{keyword}")]
                )
                buttons.append(
                    [InlineKeyboardButton(f"📂 Pages {int(index)}/{data['total']}", callback_data="pages")]
                )

                await query.edit_message_reply_markup( 
                    reply_markup=InlineKeyboardMarkup(buttons)
                )
                return
        elif query.data == "about":
            buttons = buttons = [
             [
                InlineKeyboardButton('Help 🆘', callback_data='help'),
                InlineKeyboardButton('Group Help 👥', callback_data='ghelp'),
             ],
            [
                InlineKeyboardButton('Home 🏠', callback_data='home'),
            ],
            ]
            await query.message.edit(text=ABOUT_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "help":
            buttons = buttons = [
             [
                InlineKeyboardButton('About 📄', callback_data='about'),
                InlineKeyboardButton('Group Help 👥', callback_data='ghelp'),
             ],
            [
                InlineKeyboardButton('Home 🏠', callback_data='home'),
            ],
            ]
            await query.message.edit(text=HELP_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "ghelp":
            buttons = buttons = [
             [
                InlineKeyboardButton('➕ Add Me On Your Group ➕', url='http://t.me/myKdrama_bot?startgroup=true'),
             ],             [
                InlineKeyboardButton('About 📄', callback_data='about'),
                InlineKeyboardButton('Help 🆘', callback_data='help'),
             ],
            [
                InlineKeyboardButton('Home 🏠', callback_data='home'),
            ],
            ]
            await query.message.edit(text=GHELP_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

        elif query.data == "home":
            buttons = buttons = [
            [
                InlineKeyboardButton('Search Hear 🔎', switch_inline_query_current_chat=''),
                InlineKeyboardButton('Go Inline 🔅', switch_inline_query=''),
            ],
            [
                InlineKeyboardButton('Updates Channel 🗣', url='https://t.me/SBS_Studio'),
            ],
            [
                InlineKeyboardButton("Invite Friends 👫", url="https://t.me/share/url?url=Hello%20People%F0%9F%98%8A%0A%0AAre%20you%20want%20to%20download%20more%20k-dramas%E2%9D%93%0A%0A%E2%80%A2%40myKdrama_bot%20will%20help%20you%20to%20Download%20k-dreams%20Easily%20.%0A%0AFeatures%20of%20%40myKdrama_bot%0A%20%20%20~%20Inline%20keyboard%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%20Request%20Dramas%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%20Inline%20Search%20Mode%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%2024%2A7%20Service%20%E2%9C%94%EF%B8%8F%0A%20%20%20~%20Now%20Bot%20stable%20100%25%0A%0A12%20000%2B%20episodes%20were%20available%20on%20%40myKdrama_bot%0A%0ABot%20Link%3A-%20%20%40myKdrama_bot%0A%0A%7C%20Share%20Friends%20%26%20Support%20Us%20.%20.%20.%E2%9D%A4%EF%B8%8F"),
            ],
        ]
            await query.message.edit(text=HOME_TEXT, reply_markup=InlineKeyboardMarkup(buttons), disable_web_page_preview=True)

            
        elif query.data.startswith("subinps"):
            ident, file_id = query.data.split("#")
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
                InlineKeyboardButton('Download Subtitles 🎦', url='https://t.me/TGsubtitledownloadebot'),
            ],
            [
                InlineKeyboardButton('Updates Channel 🗣', url='https://t.me/SBS_Studio'),
                InlineKeyboardButton('Rate ⭐', url='https://t.me/tlgrmcbot?start=mykdrama_bot-review'),
            ],
        ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )
        elif query.data.startswith("checksub"):
            if AUTH_CHANNEL and not await is_subscribed(client, query):
                await query.answer("I Like Your Smartness, But Don't Be Oversmart 😒",show_alert=True)
                return
            ident, file_id = query.data.split("#")
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
                    f_caption = f"{title}"
                buttons = [
             [
                InlineKeyboardButton('Download Subtitles 🎦', url='https://t.me/TGsubtitledownloadebot'),
            ],
            [
                InlineKeyboardButton('Updates Channel 🗣', url='https://t.me/SBS_Studio'),
                InlineKeyboardButton('Rate ⭐', url='https://t.me/tlgrmcbot?start=mykdrama_bot-review'),
            ],
        ]
                
                await query.answer()
                await client.send_cached_media(
                    chat_id=query.from_user.id,
                    file_id=file_id,
                    caption=f_caption,
                    reply_markup=InlineKeyboardMarkup(buttons)
                    )


        elif query.data == "pages":
            await query.answer()
    else:
        await query.answer("കൌതുകും ലേശം കൂടുതൽ ആണല്ലേ👀",show_alert=True)
