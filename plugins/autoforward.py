import os
import logging
import re
import asyncio
import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, InputMediaVideo, BotCommand
from config import Config
from database import db
from .test import CLIENT, start_clone_bot
from .settings import get_message


CLIENT = CLIENT()
API_ID = Config.API_ID
API_HASH = Config.API_HASH
DEFAULT_DELAY_BETWEEN_GROUPS = int(os.getenv("DELAY_BETWEEN_GROUPS", 5))
DEFAULT_SENDING_INTERVAL = int(os.getenv("SENDING_INTERVAL", 600))  # Interval between sending messages in seconds
DELAY_RANDOM_PERCENTAGE = int(os.getenv("DELAY_RANDOM_PERCENTAGE", 10))

# Variable to hold the message to send to all groups
message_to_send = None

# Event for controlling spam
stop_event = asyncio.Event()
spam_task = None


@Client.on_callback_query(filters.regex(r'^stspam'))
async def start_spam(client, message):
    logging.info("Al fin entro")
    try:    
        global spam_task
        user_id = message.from_user.id
        
        if spam_task and not spam_task.done():
            #await client.answer_callback_query(message.id, text = "El reenvio esta activo", show_alert=False) 
            await client.send_message(message.id, text = "El reenvio esta activo")
            return
    
        #try:
         #   delay_between_groups = int(message.text.split()[1]) #===========arreglar por planes
        #    sending_interval = int(message.text.split()[2])
        #except (IndexError, ValueError):
        delay_between_groups = DEFAULT_DELAY_BETWEEN_GROUPS
        sending_interval = DEFAULT_SENDING_INTERVAL
    
        stop_event.clear()
        spam_task = asyncio.create_task(background_message_sender(delay_between_groups, sending_interval, user_id, client))
        #await message.edit_text(f"Spam started with a {delay_between_groups}s delay between groups and {sending_interval}s sending interval.")
        await db.update_status(user_id, True)
        logging.info(f"Spam started with a {delay_between_groups}s delay and {sending_interval}s interval.")
    except Exception as e:
        logging.error(f"Al start spam: {e}")


@Client.on_callback_query(filters.regex(r'^stopspam'))
async def stop_spam(client, message):
    global spam_task
    try:
        if not (spam_task and not spam_task.done()):
            await client.answer_callback_query(message.id, text = "El reenvio esta desactivado", show_alert=False)
            await db.update_status(message.from_user.id, False)
            return
    
        stop_event.set()
        await spam_task  # Esperar a que la tarea de spam se complete
        await client.answer_callback_query(message.id, text = "El reenvio esta desactivado", show_alert=False) 
        await db.update_status(message.from_user.id, False)
        logging.info("Spam stopped.")
    except Exception as e:
        logging.error(f"Al stop spam: {e}")

    
def calculate_random_delay(base_delay):
    max_increase = (DELAY_RANDOM_PERCENTAGE / 100) * base_delay
    random_delay = base_delay + random.uniform(0, max_increase)
    return random_delay

async def set_message_to_send(client, message):
    global message_to_send
    try:
        message_to_send = await db.get_message_id(message.from_user.id)
    except Exception as e:
        logging.error(f"error al recuperar mensajes: {e}")
    logging.info("Guardados los emnsajes para reenvio")

async def send_message_to_groups(delay_between_groups, user_id, client):
    global message_to_send
    try:
        if message_to_send:
            groups = db.get_user_channels(user_id)  # Cambiar según tu implementación
            _bot = await db.get_bot(user_id)
            bot = await start_clone_bot(CLIENT.client(_bot))
            for group in groups:
                if stop_event.is_set():  # Check if the stop event is set                           #aqui tiene que mandarlo el userbot
                    logging.info("Stopping message broadcast.")  # Notificar al usuario
                    break
                try:
                    for message in message_to_send:
                        message_id = message['id']
                        message_type = message.get('type', 'single')
                        message_in_memory = await get_message(client, message)
                        if message_type == 'media_group':
                                media_group = []
                                text_messages = []
                                new_messages = []
                                
                                for msg in message_in_memory:
                                    if msg.text:
                                        text_messages.append(msg.text)
                                    elif msg.photo:
                                        photo = msg.photo[-1] if isinstance(msg.photo, list) else msg.photo
                                        media_group.append(InputMediaPhoto(media=photo.file_id, caption=msg.caption))
                                    elif msg.video:
                                        media_group.append(InputMediaVideo(media=msg.video.file_id, caption=msg.caption))                               
                                # Enviar grupo de medios
                                if media_group:
                                    sent_media = await bot.send_media_group(chat_id=group['chat_id'], media=media_group)
                        else:
                            if message_in_memory.text:
                                  await bot.send_message(
                                      text=message_in_memory.text,
                                      chat_id=group['chat_id'],
                                      #reply_markup=reply_markup    =======================  para cuando extraiga los botones
                                  )
                            elif message_in_memory.photo:
                                  photo_file_id = message_in_memory.photo[-1].file_id if isinstance(message_in_memory.photo, list) else message_in_memory.photo.file_id
                                  await bot.send_photo(
                                      chat_id=group['chat_id'],
                                      photo=photo_file_id,
                                      caption=message_in_memory.caption,
                                      #reply_markup=reply_markup
                                  )
                            elif message_in_memory.video:
                                  await bot.send_video(
                                      chat_id=group['chat_id'],
                                      video=message_in_memory.video.file_id,
                                      caption=message_in_memory.caption,
                                      #reply_markup=reply_markup
                                  )
                            logging.info(f"Message sent to group '{group.username}'")
                            delay = calculate_random_delay(delay_between_groups)
                            logging.info(f"Delay set to {delay} seconds.")
                            await asyncio.sleep(delay)  # Usar asyncio.sleep en lugar de time.sleep
                            
                except Exception as e:
                    logging.error(f"Error sending message to group '{group.username}': {e}")
    except Exception as e:
        logging.error(f"al reeenviar los mensajes por: {e}")

async def background_message_sender(delay_between_groups, sending_interval, user_id, client):
    logging.info("Background spam task started.")
    try:
        while not stop_event.is_set():
            await send_message_to_groups(delay_between_groups, user_id, client)
            if not stop_event.is_set():
                delay = calculate_random_delay(sending_interval)
                logging.info(f"Interval set to {delay} seconds.")
                await asyncio.sleep(delay)  # Usar asyncio.sleep
    except Exception as e:
        logging.error(f"Al establecer el background: {e}")
        



#====================Mensaje de forma inmendiata, desabiltado para user=========================# 
#def send_all(client: Client, message: Message):
#    if not message_to_send:
#        message.edit_text("No message has been saved. Use .addmessage to save a message.")
#        logging.warning("Attempted to send messages without a saved message.")
#        return
#    message.edit_text("Starting message broadcast to all groups...")
#    send_message_to_groups(DEFAULT_DELAY_BETWEEN_GROUPS)
#    message.edit_text("Message broadcast completed.")
#    logging.info("Message broadcast to all groups completed.")

