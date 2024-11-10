import logging
from os import environ 
from config import Config
import motor.motor_asyncio
from pymongo import MongoClient
from datetime import datetime, timedelta

async def mongodb_version():
    x = MongoClient(Config.DB_URL)
    mongodb_version = x.server_info()['version']
    return mongodb_version

class Database:
    
    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.bot = self.db.bots
        self.col = self.db.users
        self.nfy = self.db.notify
        self.chl = self.db.channels 
        
    def new_user(self, id, name, plan_type="FREE", expire_plan=None, last_time=None, forward=False ,message_ids=None):
        return dict(
            id = id,
            name = name,
            ban_status=dict(
                is_banned=False,
                ban_reason="",
            ),
            plan_type=plan_type,  # Nuevo campo
            expire_plan=expire_plan,     # Nuevo campo
            message_ids=message_ids or [],  # Nuevo campo como lista vacía por defecto
            last_time=last_time,
            forward=forward,
        )
      
    async def add_user(self, id, name, plan_type="FREE", expire_plan=None, forward=False):
        user = self.new_user(id, name, plan_type, expire_plan, forward)
        await self.col.insert_one(user)
    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'id':int(id)})
        return bool(user)
        
    async def get_user_status(self, id):
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user['forward']
        else:
            return None
    async def update_status(self, id, status):
        await self.col.update_one({'id': int(id)},{'$set': {'forward': status}})        
    
    async def get_last_time(self, id):
        user = await self.col.find_one({'id': int(id)})
        if user:
            return user['last_time']
        else:
            return None    
    async def update_last_time(self, id, time):
        await self.col.update_one({'id': int(id)},{'$set': {'last_time': time}})  
        
    async def total_users_bots_count(self):
        bcount = await self.bot.count_documents({})
        count = await self.col.count_documents({})
        return count, bcount

    async def total_channels(self):
        count = await self.chl.count_documents({})
        return count
    
    async def remove_ban(self, id):
        ban_status = dict(
            is_banned=False,
            ban_reason=''
        )
        await self.col.update_one({'id': id}, {'$set': {'ban_status': ban_status}})
    
    async def ban_user(self, user_id, ban_reason="No Reason"):
        ban_status = dict(
            is_banned=True,
            ban_reason=ban_reason
        )
        await self.col.update_one({'id': user_id}, {'$set': {'ban_status': ban_status}})

    async def get_ban_status(self, id):
        default = dict(
            is_banned=False,
            ban_reason=''
        )
        user = await self.col.find_one({'id':int(id)})
        if not user:
            return default
        return user.get('ban_status', default)

    async def get_all_users(self):
        return self.col.find({})
    
    async def delete_user(self, user_id):
        await self.col.delete_many({'id': int(user_id)})
 
    async def get_banned(self):
        users = self.col.find({'ban_status.is_banned': True})
        b_users = [user['id'] async for user in users]
        return b_users

    #---------------------------Messages---------------------#

    
    async def add_message_id(self, user_id, message_id, is_media_group=False):
        """
        Guarda un ID de mensaje o media_group_id en la base de datos
        
        Args:
            user_id (int): ID del usuario
            message_id (int/str): ID del mensaje o media_group_id
            is_media_group (bool): True si es un media_group_id, False si es un message_id
        """
        message_data = {
            'id': message_id,
            'type': 'media_group' if is_media_group else 'single',
        }
        
        await self.col.update_one(
            {'id': int(user_id)},
            {'$addToSet': {'message_ids': message_data}}
        )
    async def get_message_ids(self, user_id):
        """
        Recupera todos los mensajes guardados del usuario
        Mantiene la compatibilidad con la estructura anterior si existe
        """
        user = await self.col.find_one({'id': int(user_id)})
        if not user:
            return []
        
        message_ids = user.get('message_ids', [])
        
        # Comprueba si los message_ids son del formato antiguo (solo IDs)
        # o del nuevo formato (diccionarios con tipo)
        if message_ids and not isinstance(message_ids[0], dict):
            # Convierte los IDs antiguos al nuevo formato
            return [{'id': msg_id, 'type': 'single'} for msg_id in message_ids]
        
        return message_ids

    async def remove_message_id(self, user_id, message_id):
        """
        Elimina un mensaje de la base de datos
        """
        try:
            # Convertir a enteros
            user_id = int(user_id)
            message_id = int(message_id)
    
            # Primero intentamos eliminar el formato nuevo
            result = await self.col.update_one(
                {'id': user_id},
                {'$pull': {'message_ids': {'id': message_id}}}
            )
    
            # Si no se modificó nada, intentamos con el formato antiguo
            if result.modified_count == 0:
                await self.col.update_one(
                    {'id': user_id},
                    {'$pull': {'message_ids': message_id}}
                )
    
            logging.info(f"Mensaje {message_id} eliminado para usuario {user_id}")
        except Exception as e:
            logging.error(f"Error al eliminar mensaje: {e}")
            raise
#------------------------Plan------------------------------

    async def update_plan_type(self, user_id, plan_type):
        await self.col.update_one(
            {'id': int(user_id)},
            {'$set': {'plan_type': plan_type}}  # Asegúrate de usar plan_type
        )
    
    async def get_plan_type(self, user_id):
        user = await self.col.find_one({'id': int(user_id)})
        if user:
            return user['plan_type']
        else:
            return None

    async def update_expire_plan(self, user_id, plan_type, extend=False):
        # Validar que el tipo de plan sea válido
        valid_plans = ["FREE", "PREMIUM1", "PREMIUM2", "PREMIUM3"]
        if plan_type not in valid_plans:
            raise ValueError("Tipo de plan inválido")
    
        user = await self.col.find_one({'id': int(user_id)})
        
        if user:
            current_expire_plan = user.get('expire_plan')
            
            if plan_type == "FREE":
                new_expire_plan = None
            elif plan_type in ["PREMIUM1", "PREMIUM2", "PREMIUM3"]:
                days_mapping = {
                    "PREMIUM1": 7,
                    "PREMIUM2": 7,
                    "PREMIUM3": 30
                }
                if extend and current_expire_plan:
                    new_expire_plan = current_expire_plan + timedelta(days=30)
                else:
                    new_expire_plan = datetime.now() + timedelta(days=days_mapping[plan_type])
            
            await self.col.update_one(
                {'id': int(user_id)},
                {'$set': {'expire_plan': new_expire_plan}}
            )
        else:
            raise ValueError("Usuario no encontrado.")
#----------------------Config---------------------------

       
    async def add_bot(self, datas):
       if not await self.is_bot_exist(datas['user_id']):
          await self.bot.insert_one(datas)
    
    async def remove_bot(self, user_id):
       await self.bot.delete_many({'user_id': int(user_id)})
      
    async def get_bot(self, user_id: int):
       bot = await self.bot.find_one({'user_id': user_id})
       return bot if bot else None
                                          
    async def is_bot_exist(self, user_id):
       bot = await self.bot.find_one({'user_id': user_id})
       return bool(bot)
                                          
    async def in_channel(self, user_id: int, chat_id: int) -> bool:
       channel = await self.chl.find_one({"user_id": int(user_id), "chat_id": int(chat_id)})
       return bool(channel)
    
    async def add_channel(self, user_id: int, chat_id: int, title, username):
       channel = await self.in_channel(user_id, chat_id)
       if channel:
         return False
       return await self.chl.insert_one({"user_id": user_id, "chat_id": chat_id, "title": title, "username": username})
    
    async def remove_channel(self, user_id: int, chat_id: int):
       channel = await self.in_channel(user_id, chat_id )
       if not channel:
         return False
       return await self.chl.delete_many({"user_id": int(user_id), "chat_id": int(chat_id)})
    
    async def get_channel_details(self, user_id: int, chat_id: int):
       return await self.chl.find_one({"user_id": int(user_id), "chat_id": int(chat_id)})
       
    async def get_user_channels(self, user_id: int):
       channels = self.chl.find({"user_id": int(user_id)})
       return [channel async for channel in channels]
     
    async def get_filters(self, user_id):
       filters = []
       filter = (await self.get_configs(user_id))['filters']
       for k, v in filter.items():
          if v == False:
            filters.append(str(k))
       return filters
              
    async def add_frwd(self, user_id):
       return await self.nfy.insert_one({'user_id': int(user_id)})
    
    async def rmve_frwd(self, user_id=0, all=False):
       data = {} if all else {'user_id': int(user_id)}
       return await self.nfy.delete_many(data)
    
    async def get_all_frwd(self):
       return self.nfy.find({})
     
db = Database(Config.DB_URL, Config.DB_NAME)



