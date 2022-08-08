import os
from pyrogram import Client, filters
from bot.helpers.sql_helper import gDriveDB, idsDB
from bot.helpers.utils import CustomFilters, humanbytes, find_starttostr, find_betweentwostr
from bot.helpers.gdrive_utils import GoogleDrive 
from bot import DOWNLOAD_DIRECTORY, LOGGER
from bot.config import Messages, BotCommands
from pyrogram.errors import FloodWait, RPCError
from bot.helpers.sql_helper import idsDB


@Client.on_message(filters.private & filters.incoming & (filters.document | filters.audio | filters.video) & CustomFilters.auth_users)

def _telegram_file(client, message):
    user_id = message.from_user.id
    rname = message.caption+')'
    given_name = idsDB.search_pname(user_id)
    print(given_name)
    if given_name == 'hola':
        gname = find_starttostr(rname,0,')') + ')'
    else:
        gname = given_name + ' အပိုင်း ' + find_betweentwostr(rname, '(', ')')
    
    print(gname)

    sent_message = message.reply_text('🕵️**.ဖိုင်လင့်ကိုစစ်ဆေးနေပါသည်...**'+gname+'.mp4', quote=True)
    if message.document:
        file = message.document
    elif message.video:
        file = message.video
    elif message.audio:
        file = message.audio
    sent_message.edit(Messages.DOWNLOAD_TG_FILE.format(file.file_name, humanbytes(file.file_size), file.mime_type))
    LOGGER.info(f'Download:{user_id}: {file.file_id}')
    try:
        dl_name = os.path.join(f'{DOWNLOAD_DIRECTORY}/{gname}')
        file_path = message.download(file_name=dl_name+').mp4')
        sent_message.edit(Messages.DOWNLOADED_SUCCESSFULLY.format(os.path.basename(file_path), humanbytes(os.path.getsize(file_path))))
        msg = GoogleDrive(user_id).upload_file(file_path, file.mime_type)
        sent_message.reply_text(msg)
    except RPCError:
        sent_message.edit(Messages.WENT_WRONG)
    LOGGER.info(f'Deleteing: {file_path}')
    os.remove(file_path)
