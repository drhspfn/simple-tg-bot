# Module for work with the database
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

# DB classes
from .base_data import *

# For temporary storage of user data
from aiogram import Dispatcher
from .user_data import *

import asyncio
import sys






class APP:
    def __init__(self, database_path, config_path, user_datas_path, dp:Dispatcher=None) -> None:
        self.DB_PATH = database_path
        self.config_path = config_path
        self.DP = dp
        self.bot_config = {}
        
        """
            ABOUT `self.default_user`
                In this bot I do not need to store users in the database, 
                but if necessary, you can enter them in the database, 
                and add multi-language, shopping or other things...
        """
        self.default_user = {
            "message": {"id": 0, "chat":0},     # Place for information about the message-main menu
            "mes_to_dell": [],          # Message list for deletion, errors, user's messages...
            
        }

        self._load_config()

        self.data_storage = user_data.DataStorage(user_datas_path, self.default_user)
        self.engine = create_async_engine(f'sqlite+aiosqlite:///{self.DB_PATH}')
        self.async_session = sessionmaker(self.engine, class_=AsyncSession, expire_on_commit=False)

    """
        BOT CONFIG DATA
    """

    def token(self) -> str:
        if not self.bot_config:
            return ''
        return self.bot_config.get('bot_token', '')

    def sub_ids(self):
        if not self.bot_config:
            return ''
        return self.bot_config.get('subscribe_chat_ids', [])

    """
        OTHER BOT FUNC
    """
    def set_dp(self, dp:Dispatcher):
        self.DP = dp

    def _load_config(self):
        if not os.path.exists(self.config_path):
            default_config = {
                "bot_token": "Bot Token Here. From @BotFather",
                "subscribe_chat_ids": []
            }
            logging.log(logging.ERROR, "Config file was not found. It was re-created. Replace the necessary data in it")
            with open(self.config_path, "w") as file:
                json.dump(default_config, file)
            return sys.exit('')
        

        with open(self.config_path, "r") as file:
            self.bot_config = json.load(file)
            
    
    def buttons(self):
        def main_menu():
            return ["mainmenu buttons"]
    """
        BASE
            Functions for working with the database
            # ====================================================================== #
            If it's turnkey, everything will also be described according to your needs
    """
    async def add_new(self, new_name, new_media_data, new_media_caption, new_media_button):
        async with self.async_session() as session:
            new_news = Table_News(new_name=new_name, new_media_data=json.dumps(new_media_data),
                new_media_caption= new_media_caption, new_media_button=json.dumps(new_media_button))
            session.add(new_news)
            await session.commit()

    async def get_new_by_id(self, new_id:int):
        async with self.async_session() as session:
            stmt = sa.select(Table_News).where(Table_News.id == new_id)
            result = await session.execute(stmt)
            row = result.fetchone()
            if row:
                news = await row[0].get() 
                return news
            else:
                return None

    async def get_all_news(self):
        async with self.async_session() as session:
            result = await session.execute(sa.select(Table_News))
            rows = result.fetchall()
            return rows

    """
        USER
            config, local data, etc..
    """
    async def user_get(self, userid, key:Union[str, list]):
        return await self.data_storage.user_get(userid, key)

    async def user_set(self, userid:int, data:dict):
        return await self.data_storage.user_set(userid, data)

    async def add_to_dell(self, userid:int, message:types.Message):
        return await self.data_storage.add_to_dell(userid, message)
        
    async def del_all_mes(self, userid):
        return await self.data_storage.del_all_mes(userid)
        
    def save_users_data(self):
        return self.data_storage.save_user_datas()
    

class BotButtons(APP):
    def __init__(self) -> None:
        pass

    async def main_menu(self):
        markup = types.InlineKeyboardMarkup(row_width=3)
        keySearch = types.InlineKeyboardButton("Search", callback_data="inlineMenu_menu_goSearch")
        markup.add(keySearch)
        return markup
