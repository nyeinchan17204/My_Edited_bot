import os
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import (
    CustomFilters,
    humanbytes,
    find_starttostr,
    find_betweentwostr,
)
from bot.helpers.gdrive_utils import GoogleDrive
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
from bot.helpers.sql_helper import idsDB
from bot.helpers.fbhelper import dlink_finder, download_file

ep_num = {}

@Client.on_message(filters.private & filters.incoming & filters.text & (filters.command(BotCommands.Download) | filters.regex('^(ht|f)tp*')) & CustomFilters.auth_users)
def _download(client, message):
  user_id = message.from_user.id
  if not message.media:
    sent_message = message.reply_text('🕵️**Checking link...**', quote=True)
    if message.command:
      link = message.command[1]
    else:
      link = message.text
    if 'drive.google.com' in link:
      sent_message.edit(Messages.CLONING.format(link))
      LOGGER.info(f'Copy:{user_id}: {link}')
      msg = GoogleDrive(user_id).clone(link)
      sent_message.edit(msg)
    
    if 'facebook' in link or 'fb' in link:
      url = message.text
      try:
        link = dlink_finder(url)
        filename = os.path.basename(link)
        dl_path = DOWNLOAD_DIRECTORY
        sent_message.edit(Messages.DOWNLOADING.format(link))
        result, file_path = download_file(link, dl_path)

        if os.path.exists(file_path):
            sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
            msg = GoogleDrive(user_id).upload_file(file_path)
            sent_message.edit(msg)
            LOGGER.info(f'Deleteing: {file_path}')
            os.remove(file_path)
      except:
        sent_message = message.reply_text('🕵️**Your Facebook Link is Private & SO I Cannot Download**', quote=True)

@Client.on_message(filters.command('ep'))
async def text_msg(client, message):
        if len(message.command) > 1:
            message_ids = message.message_id + 1
            message_texts = message.text
            ep_num[message_ids] = message.command[1]
            print(ep_num)
        else:
            print('There is nothig')


@Client.on_message(
    filters.private
    & filters.incoming
    & (filters.document | filters.audio | filters.video)
    & CustomFilters.auth_users
)
def _telegram_file(client, message):
    user_id = message.from_user.id
    message_ids = message.message_id
    name_caption = message.caption
    movie_name = idsDB.search_pname(user_id)
    final_name = 'movie name'
    print(movie_name)
    if movie_name != "hola" and message_ids in ep_num:
        final_name = movie_name + " အပိုင်း(" + str(ep_num[message_ids]) + ").mp4"
    else:
        name_spliter = name_caption.splitlines()
        print(len(name_spliter))
        if len(name_spliter) > 3:
            final_name = name_spliter[0] + name_spliter[1] + name_spliter[2] + ".mp4"
        else:
            final_name = name_spliter[0] + ".mp4"
    print(final_name)
    sent_message = message.reply_text("🕵️**.ဖိုင်လင့်ကိုစစ်ဆေးနေပါသည်...**", quote=True)
    if message.document:
        file = message.document
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(final_name, humanbytes(file.file_size), file.mime_type))
    LOGGER.info(f"Download:{user_id}: {file.file_id}")
    try:
        dl_name = os.path.join(f"{DOWNLOAD_DIRECTORY}/{final_name}")
        file_path = message.download(file_name=dl_name)
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
        sent_message.reply_text(msg)
    except RPCError:
        sent_message.edit(Messages.WENT_WRONG)
    LOGGER.info(f"Deleteing: {file_path}")
    os.remove(file_path)
    if message_ids in ep_num:
        ep_num.pop(message_ids)
        print('Finish delete dir')
    else:
        print("noting input")
