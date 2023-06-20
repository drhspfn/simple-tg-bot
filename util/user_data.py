import json, os
from typing import Union
from aiogram import types
from aiogram.utils import exceptions
import logging


class DataStorage:
    def __init__(self, storage_path:str, user_default:dict) -> None:
        self.memory_storage = {}
        self.storage_path = storage_path
        self.user_default = user_default

        self.read_user_datas()

    async def user_get(self, userid, key:Union[str, list]):
        userid = int(userid)
        user_data = self.memory_storage.get(userid, None)
        if not user_data:
            await self._default_user(userid)
            return await self.user_get(userid, key)
        if isinstance(key, str):
            return user_data.get(key, {})
        elif isinstance(key, list):
            answer = {}
            for itm in key:
                answer.update({itm: user_data.get(itm, {})})
            return answer
        else:
            return user_data
        
    async def user_set(self, userid:int, data:dict):
        userid = int(userid)
        user_data = self.memory_storage.get(userid, None)
        if not user_data:
            await self._default_user(userid)
            return await self.user_get(userid, data)
        
        user_data.update(data)
        self.memory_storage.update({userid: user_data})
        return

      
    """
      This, in my case, was used as a storage in user data messages that are to be deleted because the menu was on the inline buttons, 
      and so as not to clutter up the chat, delete various errors and notifications
    """
    async def add_to_dell(self, userid:int, message:types.Message):
        userid = int(userid)
        user_data = self.memory_storage.get(userid, None)
        if not user_data:
            await self._default_user(userid)
            return await self.add_to_dell(userid, message)
        
        user_data['mes_to_dell'].append(message)
        self.memory_storage.update(user_data)
        return
        
    async def del_all_mes(self, userid):
        userid = int(userid)
        user_data = self.memory_storage.get(userid, None)
        if not user_data:
            await self._default_user(userid)
            return await self.del_all_mes(userid)
        
        if user_data['mes_to_dell']:
            for message_id in range(len(user_data['mes_to_dell'])):
                try:
                    await user_data['mes_to_dell'][message_id].delete()
                except exceptions.MessageToDeleteNotFound:
                    continue

            user_data['mes_to_dell'].clear()
            return self.memory_storage.update(user_data)
    
    async def _default_user(self, userid):
        userid = int(userid)
        self.memory_storage.update({userid: self.user_default})
        return 
    
    def save_user_datas(self):
        all_data = self.memory_storage
        try:
            with open(self.storage_path, "w") as file:
                json.dump(all_data, file)
                logging.log(logging.INFO, "User data successfully saved locally")
                return True
        except Exception as exc:
            logging.log(logging.ERROR, f"User data has not been saved. Error: \n{str(exc)}")
            print(str(exc))
            return False

    def read_user_datas(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as file:
                    old_users_data = json.load(file, object_hook=lambda d: {int(k) if k.lstrip('-').isdigit() else k: v for k, v in d.items()})
                    logging.log(logging.INFO, "Local user data were found and loaded")
                    self.memory_storage = old_users_data
                return True
            except json.decoder.JSONDecodeError:
                self.save_user_datas()
        else:
            return False
