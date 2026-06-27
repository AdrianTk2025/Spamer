# |========> Import necessary libraries <========|
import random
from pyrogram import Client, filters, enums
from pyrogram.enums import ChatType
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pysondb import db

# |========> Config telegram account <========|
logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

with open("api_hash_code.txt", "r", encoding='utf8') as api_hash_code:
    data = api_hash_code.readline().split(":")
    api_id = data[0]
    hash_id = data[1]
app = Client("session_file", api_id=api_id, api_hash=hash_id)

# |========> Global variables <========|

main_admin_id = 8544499611

is_off = False

typing_ids = []

intro_text = ""

# |========> Setup config.json <========|
ConfigAcc = db.getDb('config.json')

# Get account info from config.json
check = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})

# Keep default config
default_config = {
    'fosh_list': [],
    'enemy_list': [],
    'silence_list': [],
    'spam_list': [],
    'spam_time': 5,
    'enemy_reply': 1,
    'main_admin_id': main_admin_id
}

# Add account default config to config.json if it not exists
if not check:
    ConfigAcc.add(default_config)

# |========> Setup scheduler <========|
scheduler = AsyncIOScheduler()
scheduler.start()


# |========> New Message Handler <========|
@app.on_message(filters.command('ping'))
async def new_message_handler(client,message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    txt = "__𖤍𝐀𝐑𝐓𝐈𝐍 𝐎𝐍𝐋𝐈𝐍𝐄𖤍__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('help'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    txt = """
👑Online bot ArTin'Iranshahri👑

 ⚜️`/ping`

On is Off
 ⚜️`/bot`   (off | on)

Restart
 ⚜️`/restart`

aspem Time
⚜️`/settime`   (num)

user Group.account
 ⚜️`/id`  (group | pv | reply)

reply
 ⚜️`/reply`   (on | off)

Yayping
⚜️`/typing`   (on | off)

Add Text
⚜️`/addfosh`  (reply)

Add Kheshab (texet)
⚜️`/addallfosh`  (reply)

deltaxet
⚜️`/delfosh`  (reply)

List Fosh
⚜️`/flist`
┅
delFosh
 ⚜️`/cleanflist`
┅
add enemy
⚜️`/setenemy`   (id | pv | reply)

Del Enemy
⚜️`/delenemy`   

List Enemy
⚜️`/enemylist`
┅
Del Lust Enemy
⚜️`/cleanelist`

Off Eco
⚜️`/add`   (id)

Del Eco
⚜️`/del`   (id)

List Eco
⚜️`/dellist`
┅
Spam Set
⚜️`/setspam`   (id | group | pv | reply)

Spam List
⚜️`/spamlist`

Del Spam list
⚜️`/cleanslist`

Texet Spam
⚜️`/settext`   (text)

 del Taxer
⚜️`/deltext`
┅
𖣐𝐀𝐝𝐦𝐢𝐧: t.me/Wilson_ir 𖣐
"""

    await message.reply(txt, quote=True)


@app.on_message(filters.command('bot'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()
    if len(msg) != 2:
        return
    msg = msg[1]

    if msg == "on":
        if is_off:
            is_off = False
            txt = "__ربات روشن شد!__"
        else:
            txt = "__ربات روشن بوده است!__"

    elif msg == "off":
        if is_off:
            txt = "__ربات خاموش بوده است!__"
        else:
            is_off = True
            txt = "__ربات خاموش شد!__"

    else:
        return

    await message.reply(txt, quote=True)


@app.on_message(filters.command('settime'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()
    if len(msg) != 2:
        return
    msg = msg[1]
    try:
        msg = int(msg)
    except ValueError:
        return

    if msg < 1:
        txt = "__مقدار ورودی نامعتبر است!__"

    else:
        # Update config
        ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'spam_time': msg})

        txt = f"__تاخیر بین هر اسپم با موفقیت به {msg} ثانیه تغییر یافت!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('id'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    if message.reply_to_message is not None:
        given_id = message.reply_to_message.from_user.id

        txt = f"__آیدی عددی کاربر ریپلای شده  :  `{given_id}`__"

    else:
        if message.chat.type is ChatType.PRIVATE:
            txt = f"__آیدی عددی این کاربر  :  `{message.chat.id}`__"

        elif message.chat.type is ChatType.SUPERGROUP:
            txt = f"__آیدی عددی این گروه  :  `{message.chat.id}`__"

        else:
            txt = "__لطفا در گروه یا پیوی کاربر ارسال کنید!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('reply'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    msg = message.text
    msg = msg.split()
    if len(msg) != 2:
        return
    msg = msg[1]

    if msg == "on":
        if datas['enemy_reply']:
            txt = "__ریپلای روشن بوده است!__"

        else:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'enemy_reply': 1})

            txt = "__ریپلای روشن شد!__"

    elif msg == "off":
        if datas['enemy_reply']:
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'enemy_reply': 0})

            txt = "__ریپلای خاموش شد!__"

        else:
            txt = "__ریپلای خاموش بوده است!__"

    else:
        return

    await message.reply(txt, quote=True)


@app.on_message(filters.command('typing'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off
    global typing_ids

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()
    if len(msg) != 2:
        return
    msg = msg[1]

    if msg == "on":
        this_job = scheduler.get_job(job_id="typing")
        if this_job is None:
            scheduler.add_job(typing_job, "interval", seconds=5, id="typing")

        if message.chat.id not in typing_ids:
            typing_ids.append(message.chat.id)
            txt = "__حالت تایپینگ در اینجا روشن شد!__"
        else:
            txt = "__حالت تایپینگ در اینجا روشن بوده است!__"

    elif msg == "off":
        if message.chat.id in typing_ids:
            typing_ids.remove(message.chat.id)
            txt = "__حالت تایپینگ در اینجا خاموش شد!__"
        else:
            txt = "__حالت تایپینگ در اینجا خاموش بوده است!__"

        if len(typing_ids) == 0:
            this_job = scheduler.get_job(job_id="typing")
            if this_job is not None:
                scheduler.remove_job(job_id="typing")

    else:
        return

    await message.reply(txt, quote=True)


async def typing_job():
    global typing_ids
    global is_off

    if is_off:
        return

    for typing_id in typing_ids:
        try:
            await app.send_chat_action(typing_id, enums.ChatAction.TYPING)
        except:
            typing_ids.remove(typing_id)


@app.on_message(filters.command('addfosh'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id or message.reply_to_message is None:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.reply_to_message.text not in datas['fosh_list']:
        datas['fosh_list'].append(message.reply_to_message.text)
        # Update config
        ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'fosh_list': datas['fosh_list']})
        txt = "__متن ریپلای شده به لیست فحش ها اضافه شد!__"

    else:
        txt = "__متن ریپلای شده در لیست فحش ها بوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('addallfosh'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id or message.reply_to_message is None:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    msg = message.reply_to_message.text
    all_fosh = msg.split('\n')

    for fosh in all_fosh:
        if fosh not in datas['fosh_list']:
            datas['fosh_list'].append(fosh)
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'fosh_list': datas['fosh_list']})

    txt = "__همه فحش های متن ریپلای شده به لیست فحش ها اضافه شد!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('delfosh'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id or message.reply_to_message is None:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if message.reply_to_message.text in datas['fosh_list']:
        datas['fosh_list'].remove(message.reply_to_message.text)
        # Update config
        ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'fosh_list': datas['fosh_list']})
        txt = "__متن ریپلای شده از لیست فحش ها حذف شد!__"

    else:
        txt = "__متن ریپلای شده در لیست فحش ها نبوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('flist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if len(datas['fosh_list']) == 0:
        txt = "__لیست فحش خالی است!__"

    else:
        txt = "__🔰 لیست فحش ها بصورت زیر است:\n(برای کپی کردن روی آن کلیک کنید)__\n\n"

        i = 1
        for fosh in datas['fosh_list']:
            txt += f"\n{i}. `{fosh}`\n"
            i += 1

    await message.reply(txt, quote=True)


@app.on_message(filters.command('cleanflist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'fosh_list': []})

    await message.reply("__لیست فحش ها با موفقیت خالی شد!__", quote=True)


@app.on_message(filters.command('restart'))
async def new_message_handler(client, message):
    global main_admin_id
    global default_config

    if message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, default_config)

    await message.reply("__ربات ریستارت شد!__", quote=True)


@app.on_message(filters.command('setenemy'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 1:
        if message.reply_to_message is not None:
            given_id = message.reply_to_message.from_user.id
            txt = "__کاربر ریپلای شده با موفقیت به لیست دشمن اضافه شد!__"

        elif message.chat.type is ChatType.PRIVATE:
            given_id = message.chat.id
            txt = "__این کاربر با موفقیت به لیست دشمن اضافه شد!__"

        else:
            given_id = 0
            txt = "__لطفا دستور را در پیوی شخص موردنظر ارسال کنید یا روی آن ریپلای کنید و ارسال کنید ویا آیدی عددی کاربر مدنظر را جلوی دستور قرار دهید!__"

    elif len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت به لیست دشمن اضافه شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور افزودن دشمن به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

        if given_id not in datas['enemy_list']:
            datas['enemy_list'].append(given_id)
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'enemy_list': datas['enemy_list']})
        else:
            txt = "__کاربر موردنظر در لیست دشمن بوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('delenemy'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 1:
        if message.reply_to_message is not None:
            given_id = message.reply_to_message.from_user.id
            txt = "__کاربر ریپلای شده با موفقیت از لیست دشمن حذف شد!__"

        elif message.chat.type is ChatType.PRIVATE:
            given_id = message.chat.id
            txt = "__این کاربر با موفقیت از لیست دشمن حذف شد!__"

        else:
            given_id = 0
            txt = "__لطفا دستور را در پیوی شخص موردنظر ارسال کنید یا روی آن ریپلای کنید و ارسال کنید ویا آیدی عددی کاربر مدنظر را جلوی دستور قرار دهید!__"

    elif len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت از لیست دشمن حذف شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور حذف دشمن به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

        if given_id in datas['enemy_list']:
            datas['enemy_list'].remove(given_id)
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'enemy_list': datas['enemy_list']})
        else:
            txt = "__کاربر موردنظر در لیست دشمن نبوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('enemylist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if len(datas['enemy_list']) == 0:
        txt = "__لیست دشمن خالی است!__"

    else:
        txt = "__🔰 لیست دشمن ها بصورت زیر است:\n(برای کپی کردن روی آن کلیک کنید)__\n\n"

        i = 1
        for enemy_id in datas['enemy_list']:
            txt += f"\n{i}. `{enemy_id}`"
            i += 1

    await message.reply(txt, quote=True)


@app.on_message(filters.command('add'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت به لیست سکوت اضافه شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور افزودن به لیست سکوت به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

        if given_id not in datas['silence_list']:
            datas['silence_list'].append(given_id)
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'silence_list': datas['silence_list']})
        else:
            txt = "__کاربر موردنظر در لیست سکوت بوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('del'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت از لیست سکوت حذف شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور حذف از لیست سکوت به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

        if given_id in datas['silence_list']:
            datas['silence_list'].remove(given_id)
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'silence_list': datas['silence_list']})
        else:
            txt = "__کاربر موردنظر در لیست سکوت نبوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('dellist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if len(datas['silence_list']) == 0:
        txt = "__لیست سکوت خالی است!__"

    else:
        txt = "__🔰 لیست سکوت بصورت زیر است:\n(برای کپی کردن روی آن کلیک کنید)__\n\n"

        i = 1
        for silence_id in datas['silence_list']:
            txt += f"\n{i}. `{silence_id}`"
            i += 1

    await message.reply(txt, quote=True)


@app.on_message(filters.command('cleanelist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'enemy_list': []})

    await message.reply("__لیست دشمن ها با موفقیت خالی شد!__", quote=True)


@app.on_message(filters.command('setspam'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    msg = message.text
    msg = msg.split()

    if len(msg) == 1:
        if message.reply_to_message is not None:
            given_id = message.reply_to_message.from_user.id
            txt = "__کاربر ریپلای شده با موفقیت به لیست اسپم اضافه شد!__"

        elif message.chat.type is ChatType.PRIVATE:
            given_id = message.chat.id
            txt = "__این کاربر با موفقیت به لیست اسپم اضافه شد!__"

        elif message.chat.type is ChatType.SUPERGROUP:
            given_id = message.chat.id
            txt = "__این گروه با موفقیت به لیست اسپم اضافه شد!__"

        else:
            given_id = 0
            txt = "__لطفا دستور را در پیوی شخص یا گروه موردنظر ارسال کنید یا روی شخص ریپلای کنید و ارسال کنید ویا آیدی عددی کاربر یا گروه مدنظر را جلوی دستور قرار دهید!__"

    elif len(msg) == 2:
        given_id = msg[1]
        try:
            given_id = int(given_id)
            txt = "__آیدی عددی داده شده با موفقیت به لیست اسپم اضافه شد!__"
        except ValueError:
            given_id = 0
            txt = "__آیدی عددی وارد شده نامعتبر است!__"

    else:
        given_id = 0
        txt = "__دستور افزودن به لیست اسپم به شکل نادرستی وارد شده است!__"

    if given_id != 0:
        # Get account info from config
        datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

        this_job = scheduler.get_job(job_id="spam")
        if this_job is None:
            scheduler.add_job(spam_job, "interval", seconds=datas['spam_time'], id="spam")

        if given_id not in datas['spam_list']:
            datas['spam_list'].append(given_id)
            # Update config
            ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'spam_list': datas['spam_list']})
        else:
            txt = "__آیدی عددی موردنظر در لیست اسپم بوده است!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('spamlist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if len(datas['spam_list']) == 0:
        txt = "__لیست اسپم خالی است!__"

    else:
        txt = "__🔰 لیست اسپم بصورت زیر است:\n(برای کپی کردن روی آن کلیک کنید)__\n\n"

        i = 1
        for spam_id in datas['spam_list']:
            txt += f"\n{i}. `{spam_id}`"
            i += 1

    await message.reply(txt, quote=True)


@app.on_message(filters.command('cleanslist'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    # Update config
    ConfigAcc.updateByQuery({'main_admin_id': main_admin_id}, {'spam_list': []})

    this_job = scheduler.get_job(job_id="spam")
    if this_job is not None:
        scheduler.remove_job(job_id="spam")

    await message.reply("__لیست اسپم با موفقیت خالی شد!__", quote=True)


async def spam_job():
    global intro_text
    global is_off

    if is_off:
        return

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    for spam_id in datas['spam_list']:
        if len(datas['fosh_list']) == 0:
            txt = "__لیست فحش ها خالی است!__"
        else:
            txt = intro_text + random.choice(datas['fosh_list'])

        try:
            await app.send_message(chat_id=spam_id, text=txt)
        except:
            pass


@app.on_message(filters.command('settext'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off
    global intro_text

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    if message.reply_to_message is None:
        msg = message.text
        msg = msg.replace("/settext ", "")
        intro_text = msg
        txt = "__متن پیشفرض با موفقیت تغییر یافت!__"
    else:
        replied_user = message.reply_to_message.from_user
        intro_text = f"[{replied_user.first_name}](tg://user?id={replied_user.id})  "
        txt = "__متن پیشفرض با موفقیت به تگ کردن کاربر ریپلای شده تغییر یافت!__"

    await message.reply(txt, quote=True)


@app.on_message(filters.command('deltext'))
async def new_message_handler(client, message):
    global main_admin_id
    global is_off
    global intro_text

    if is_off or message.from_user is None or message.from_user.id != main_admin_id:
        return

    intro_text = ""

    await message.reply("__متن پیشفرض با موفقیت حذف شد!__", quote=True)


@app.on_message()
async def new_message_handler(client, message):
    global intro_text
    global is_off

    # Get account info from config
    datas = ConfigAcc.getByQuery({'main_admin_id': main_admin_id})[0]

    if is_off or message.from_user is None:
        return

    # Enemy Action
    if message.from_user.id in datas['enemy_list']:

        if len(datas['fosh_list']) == 0:
            txt = "__لیست فحش ها خالی است!__"
        else:
            txt = intro_text + random.choice(datas['fosh_list'])

        try:
            if datas['enemy_reply']:
                await message.reply(txt, quote=True)
            else:
                await app.send_message(chat_id=message.chat.id, text=txt)
        except:
            pass

    # Silence Action
    if message.from_user.id in datas['silence_list']:
        try:
            await message.delete()
        except:
            pass


# |========> Run app <========|
app.run()
