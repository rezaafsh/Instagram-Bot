#MIT License

#Copyright (c) 2021 subinps

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.

#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from config import Config
from instaloader import Profile
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
import os
from utils import *

USER=Config.USER
OWNER=Config.OWNER
HOME_TEXT_OWNER=Config.HOME_TEXT_OWNER
HELP=Config.HELP
HOME_TEXT=Config.HOME_TEXT
session=f"./{USER}"
STATUS=Config.STATUS

insta = Config.L
buttons=InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton("آیدی من", url='https://t.me/rezaaf76'),
            InlineKeyboardButton("کانال من", url="https://t.me/rezaafsh")
        ]					
    ]
    )




@Client.on_message(filters.command("posts") & filters.private)
async def post(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("اول باید وارد حساب کاربری بشین /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    await bot.send_message(
            message.from_user.id,
            f"چه پست هایی رو میخوای دانلود کنی؟",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("Photos", callback_data=f"photos#{username}"),
                        InlineKeyboardButton("Videos", callback_data=f"video#{username}")
                    ]
                ]
            )
        )
    

@Client.on_message(filters.command("igtv") & filters.private)
async def igtv(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("اول باید وارد حساب کاربری بشی.. /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching IGTV from <code>@{username}</code>")
    profile = Profile.from_username(insta.context, username)
    igtvcount = profile.igtvcount
    await m.edit(
        text = f"دانلود تمام پست های IGTv؟\nتعداد این پست: {igtvcount} .",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Yes", callback_data=f"yesigtv#{username}"),
                    InlineKeyboardButton("No", callback_data=f"no#{username}")
                ]
            ]
        )
        )
    


@Client.on_message(filters.command("followers") & filters.private)
async def followers(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("اول باید وارد حسابت بشی /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"دریافت لیست فالوور <code>@{username}</code>")
    chat_id=message.from_user.id
    f = profile.get_followers()
    followers=f"**Followers List for {name}**\n\n"
    for p in f:
        followers += f"\n[{p.username}](www.instagram.com/{p.username})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"**Followers List for {name}**\n\n"
        f = profile.get_followers()
        for p in f:
            followers += f"\nName: {p.username} :     لینک پروفایل: www.instagram.com/{p.username}"
        text_file = open(f"{username}'s followers.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s followers.txt", caption=f"{name}'s followers\n\nA Project By (https://t.me/rezaafsh)")
        os.remove(f"./{username}'s followers.txt")


@Client.on_message(filters.command("followees") & filters.private)
async def followees(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("اول وارد حسابت باید بشی /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "عمومی نیست" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"دریافت لیست فالوور<code>@{username}</code>")
    chat_id=message.from_user.id
    f = profile.get_followees()
    followees=f"**Followees List for {name}**\n\n"
    for p in f:
        followees += f"\n[{p.username}](www.instagram.com/{p.username})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followees)
    except MessageTooLong:
        followees=f"**Followees List for {name}**\n\n"
        f = profile.get_followees()
        for p in f:
            followees += f"\nName: {p.username} :     Link to Profile: www.instagram.com/{p.username}"
        text_file = open(f"{username}'s followees.txt", "w")
        text_file.write(followees)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s followees.txt", caption=f"{name}'s followees\n\nA Project By (https://t.me/rezaafsh)")
        os.remove(f"./{username}'s followees.txt")




@Client.on_message(filters.command("fans") & filters.private)
async def fans(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("اول باید وارد حسابت بشی/login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "حساب شخصی" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"دریافت لیست فالوینگ ها")
    chat_id=message.from_user.id
    f = profile.get_followers()
    fl = profile.get_followees()
    flist=[]
    fmlist=[]
    for fn in f:
        u=fn.username
        flist.append(u)
    for fm in fl:
        n=fm.username
        fmlist.append(n)

    fans = [value for value in fmlist if value in flist]
    print(len(fans))
    followers=f"**Fans List for {name}**\n\n"
    for p in fans:
        followers += f"\n[{p}](www.instagram.com/{p})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"**Fans List for {name}**\n\n"
        
        for p in fans:
            followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
        text_file = open(f"{username}'s fans.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s fans.txt", caption=f"{name}'s fans\n\nA Project By (https://t.me/rezaafsh)")
        os.remove(f"./{username}'s fans.txt")


@Client.on_message(filters.command("notfollowing") & filters.private)
async def nfans(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    profile = Profile.from_username(insta.context, username)
    name=profile.full_name
    m=await message.reply_text(f"Fetching list of followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>.")
    chat_id=message.from_user.id
    f = profile.get_followers()
    fl = profile.get_followees()
    flist=[]
    fmlist=[]
    for fn in f:
        u=fn.username
        flist.append(u)
    for fm in fl:
        n=fm.username
        fmlist.append(n)

    fans = list(set(fmlist) - set(flist))
    print(len(fans))
    followers=f"**Followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>**\n\n"
    for p in fans:
        followers += f"\n[{p}](www.instagram.com/{p})"
    try:
        await m.delete()
        await bot.send_message(chat_id=chat_id, text=followers)
    except MessageTooLong:
        followers=f"Followees of <code>@{username}</code> who is <b>not</b> following <code>@{username}</code>\n\n"
        for p in fans:
            followers += f"\nName: {p} :     Link to Profile: www.instagram.com/{p}"
        text_file = open(f"{username}'s Non_followers.txt", "w")
        text_file.write(followers)
        text_file.close()
        await bot.send_document(chat_id=chat_id, document=f"./{username}'s Non_followers.txt", caption=f"{name}'s Non_followers\n\nA Project By (https://t.me/rezaafsh)")
        os.remove(f"./{username}'s Non_followers.txt")





@Client.on_message(filters.command("feed") & filters.private)
async def feed(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    count=None
    if " " in text:
        cmd, count = text.split(' ')
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m=await message.reply_text(f"Fetching Posts in Your Feed.")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    if count:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed",
            "--count", count
            ]
    else:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "--sessionfile", session,
            "--dirname-pattern", dir,
            ":feed"
            ]

    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)



@Client.on_message(filters.command("saved") & filters.private)
async def saved(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    count=None
    if " " in text:
        cmd, count = text.split(' ')
    m=await message.reply_text(f"Fetching your Saved Posts.")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    if count:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved",
            "--count", count
            ]
    else:
        command = [
            "instaloader",
            "--no-metadata-json",
            "--no-compress-json",
            "--no-profile-pic",
            "--no-posts",
            "--no-captions",
            "--no-video-thumbnails",
            "--login", USER,
            "-f", session,
            "--dirname-pattern", dir,
            ":saved"
            ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)




@Client.on_message(filters.command("tagged") & filters.private)
async def tagged(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching the posts in which <code>@{username}</code> is tagged.")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--tagged",
        "--no-captions",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)



@Client.on_message(filters.command("story") & filters.private)
async def story(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    text=message.text
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching stories of <code>@{username}</code>")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--stories",
        "--no-captions",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)



@Client.on_message(filters.command("stories") & filters.private)
async def stories(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    m=await message.reply_text(f"Fetching stories of all your followees")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-captions",
        "--no-posts",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        ":stories"
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)




@Client.on_message(filters.command("highlights") & filters.private)
async def highlights(bot, message):
    if str(message.from_user.id) != OWNER:
        await message.reply_text(
            HOME_TEXT.format(message.from_user.first_name, message.from_user.id, USER, USER, USER, OWNER),
            reply_markup=buttons,
			disable_web_page_preview=True
        )
        return
    username=USER
    if 1 not in STATUS:
        await message.reply_text("You Must Login First /login ")
        return
    text=message.text
    if " " in text:
        cmd, username = text.split(' ')
        profile = Profile.from_username(insta.context, username)
        is_followed = yes_or_no(profile.followed_by_viewer) 
        type = acc_type(profile.is_private)
        if type == "🔒Private🔒" and is_followed == "No":
            await message.reply_text("متاسفم!\nاین حساب کاربری عمومی نیست ولی اگر اکانتی داری که باهاش این رو فالو کردی میتونی با اون لاگین کنی <code>@{username}</code>.")
            return
    m=await message.reply_text(f"Fetching highlights from profile <code>@{username}</code>")
    chat_id=message.from_user.id
    dir=f"{chat_id}/{username}"
    await m.edit("Starting Downloading..\nThis may take longer time Depending upon number of posts.")
    command = [
        "instaloader",
        "--no-metadata-json",
        "--no-compress-json",
        "--no-profile-pic",
        "--no-posts",
        "--highlights",
        "--no-captions",
        "--no-video-thumbnails",
        "--login", USER,
        "-f", session,
        "--dirname-pattern", dir,
        "--", username
        ]
    await download_insta(command, m, dir)
    await upload(m, bot, chat_id, dir)

