import signal, sys
from aiogram import Dispatcher, Bot, executor, types
from util import *

bot_buttons = BotButtons()
bot_util = APP("./database.db", './config.json', './util/user_data.json')
bot = Bot(token=bot_util.token(), parse_mode="html", disable_web_page_preview=True, timeout=30)
dp = Dispatcher(bot)
bot_util.set_dp(dp)

def shutdown(signal, frame):
    loop = asyncio.get_event_loop()
    loop.stop()
    bot_util.save_users_data()
    return sys.exit('Intercept CTRL + C. Exit...')

signal.signal(signal.SIGINT, shutdown)


  
@dp.message_handler(commands=['start'])
async def handler_message_start(message: types.Message):
    return #await sendMainMenu(message)


@dp.callback_query_handler(lambda c: c.data and c.data.startswith('inlineMenu_'))
async def handler_all_inline(callback_query: types.CallbackQuery):
    userid = callback_query.message.from_id
    username = callback_query.message.from_user.first_name
    dataStrip = callback_query.data.split("_")

    inlineType = dataStrip[1]
    inlineData = dataStrip[2]
    
    #main_menu_data = await bot_util.user_get(userid, 'message')


    if inlineType == "menu":
        pass

    


async def update_menu(message:types.Message, messageContent:str, markup, userid:int=None, username:str=None, update:bool=False):
    userid = userid if userid else message.from_user.id
    username = username if username else message.from_user.first_name                  

    main_menu_data = await bot_util.user_get(userid, 'message')

    if not main_menu_data.get('id', 0):
        newMessage = await bot.send_message(message.chat.id, messageContent, "html", reply_markup=markup)
        await bot_util.user_set(userid, {'message': {'id': newMessage.message_id, "chat": newMessage.chat.id}})
        try: await message.delete()
        except: pass
        return 

    await bot_util.del_all_mes(userid)


    if await bot_util.user_get(userid, "updateMenu") or update:
        newMessage = await bot.send_message(main_menu_data['chat'], messageContent, "html", reply_markup=markup)
        await bot.delete_message(main_menu_data['chat'], main_menu_data['id'])
        if not message.audio:
            try:await message.delete()
            except: pass
        return await bot_util.user_set(userid, {'message': {'id': newMessage.message_id, "chat": newMessage.chat.id}, 'updateMenu': False})
    else:
        try:
            return await bot.edit_message_text(messageContent, main_menu_data['chat'], main_menu_data['id'], parse_mode="html", reply_markup=markup) 
        except exceptions.MessageToEditNotFound:
            await bot_util.user_set(userid, {'message': {'id': 0, "chat": 0}})
            #return await sendMainMenu(message, userid, username, update)
        except exceptions.ChatNotFound:
            return
        except exceptions.BotBlocked:
            return
        except exceptions.ChatAdminRequired:
            return 
        except exceptions.RetryAfter as e:
            return 
        except exceptions.NetworkError:
            return 
        except exceptions.TelegramAPIError as err: 
            if str(err).find('Message is not modified') != -1:
                await bot_util.user_set(userid, {'message': {'id': 0, "chat": 0}})
                newMessage = await bot.send_message(main_menu_data['chat'], messageContent, "html", reply_markup=markup)
                await bot.delete_message(main_menu_data['chat'], main_menu_data['id'])
                if not message.audio:
                    try:await message.delete()
                    except: pass
                return await bot_util.user_set(userid, {'message': {'id': newMessage.message_id, "chat": newMessage.chat.id}, 'updateMenu': False})
            else:
                return

"""
Attempting to implement a check on the let on sponsored channels. 

unsuccessful....

async def sub_Chech(message: types.Message, userid:int=None, username:str=None):
    userid = userid if userid else message.from_user.id
    username = username if username else message.from_user.first_name                  

    channel_sub = {}
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup_keys = []
    notAllowed = False

    check_data = bot_util.sub_ids()
    for chat in check_data:
        channel_info = await bot.get_chat_member(chat['chat_id'], userid)
        if channel_info.status == types.ChatMemberStatus.MEMBER or channel_info.status == types.ChatMemberStatus.OWNER or channel_info.status == types.ChatMemberStatus.CREATOR:
            markup_keys.append(types.InlineKeyboardButton(f"{chat['text']}: ✅", callback_data="inlineMenu_sub_ok"))
            channel_sub.update({chat['chat_id']: True})
        else:
            notAllowed = True
            markup_keys.append(types.InlineKeyboardButton(f"{chat['text']}: ❌", url=chat['link']))
            channel_sub.update({chat['chat_id']: False})
    markup.add(*markup_keys)
    markup.add(types.InlineKeyboardButton("Check", callback_data="inlineMenu_sub_check"))
    if notAllowed:
        messageContent = "You are not yet subscribed to one or more of our sponsors"
        return await update_menu(message, messageContent, markup, userid, username)
    else:
        messageContent = "main menu"
        return await update_menu(message, messageContent, markup, userid, username)


"""
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
