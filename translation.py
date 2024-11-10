
import os
from config import Config

class Translation(object):
  START_TXT = """<b>👋 𝚁𝚎𝚗𝚟𝚒𝚎𝚗𝚍𝚘 𝚊𝚕 𝚋𝚘𝚝, {}!</b>

<i>𝙿𝚊𝚛𝚊 𝚛𝚎𝚎𝚗𝚟𝚒𝚊𝚛 𝚖𝚎𝚜𝚊𝚓𝚎𝚜 𝚎𝚗 𝚝𝚞𝚜 𝚐𝚛𝚞𝚙𝚘𝚜 𝚌𝚘𝚖𝚘 𝚜𝚒 𝚏𝚞𝚎𝚜 𝚝𝚞́, 𝚍𝚎𝚋𝚎𝚜 𝚒𝚗𝚒𝚌𝚒𝚊𝚛 𝚜𝚎𝚜𝚒𝚘́𝚗 𝚙𝚛𝚒𝚖𝚎𝚛𝚘.

𝙿𝚞𝚎𝚍𝚎𝚜 𝚎𝚕𝚒𝚖𝚒𝚗𝚊𝚛 𝚝𝚞 𝚒𝚗𝚏𝚘𝚛𝚖𝚊𝚌𝚒𝚘́𝚗 𝚖𝚊́𝚜 𝚊𝚍𝚎𝚕𝚊𝚗𝚝𝚎 𝚌𝚞𝚊𝚗𝚍𝚘 𝚚𝚞𝚒𝚎𝚛𝚊𝚜.</i>
"""
  START_TXT_ADMIN = """<b> 👋 Hola Master {}!</b>

 <b> Que vamos a hacer hoy?</b>
"""
  START_TXT_USER = """"<b>👋 ¡Hola, {}!</b>
       Bienvenido al Panel de Administración. Aquí podrás gestionar configuraciones y funciones.
       🔧 **Funciones:**
       ► ▶️ Iniciar - Reanuda el reenvio de mensajes a los grupos
       ► 🛑 Stop - Deja de reenviar mensajes a los grupos
       ► 🤖 Userbot - Admisnistrar sesión de userbot
       ► 💬 Mensajes - Gestionar los mensajes
       ► ⚙️ Ajustes - Ajustes tiempo de reenvio(No disponible en plan FREE)
       ► 💲 Planes - Comprar un plan
       <b>Selecciona una opción del menú para comenzar.</b>
 """

  HELP_TXT = """<b><u>🔆 HELP</b></u>

<u>**📚 Available commands:**</u>
<b>⏣ __/start - check I'm alive__ 
⏣ __/forward - forward messages__
⏣ __/settings - configure your settings__
⏣ __/reset - reset your settings__</b>

<b><u>💢 Features:</b></u>
<b>► __Forward message from public channel to your channel without admin permission. if the channel is private need admin permission__
► __Forward message from private channel to your channel by using userbot(user must be member in there)__
► __custom caption__
► __custom button__
► __support restricted chats__
► __skip duplicate messages__
► __filter type of messages__
► __skip messages based on extensions & keywords & size__</b>
"""
  
  HOW_USE_TXT = """<b><u>⚠️ Before Forwarding :</b></u>
  
► __Add A Bot Or Userbot__
► __Add Atleast One To Channel (Your Bot/Userbot Must Be Admin In There)__
► __You Can Add Chats Or Bots By Using /settings__
► __If The **From Channel** Is Private Your Userbot Must Be Member In There Or Your Bot Must Need Admin Permission In There Also__
► __Then Use /forward To Forward Messages__"""
  
  ABOUT_TXT = """<b>╔════❰ ғᴏʀᴡᴀʀᴅ ʙᴏᴛ ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼📃ʙᴏᴛ : <a href=https://t.me/DeathAutoForwarderBot>ғᴏʀᴡᴀʀᴅ ʙᴏᴛ</a>
║┣⪼👦ᴄʀᴇᴀᴛᴏʀ : <a href=https://t.me/TryToLiveAlon>ᴅᴇᴀᴛʜ ᴄᴏᴍᴍᴜɴɪᴛʏ</a>
║┣⪼📡ʜᴏsᴛᴇᴅ ᴏɴ : <a href=https://heroku.com>ʜᴇʀᴏᴋᴜ</a>
║┣⪼🗣️ʟᴀɴɢᴜᴀɢᴇ : ᴘʏᴛʜᴏɴ3
║┣⪼📚ʟɪʙʀᴀʀʏ : ᴘʏʀᴏɢʀᴀᴍ ᴀsʏɴᴄɪᴏ 2.0.0 
║┣⪼🗒️ᴠᴇʀsɪᴏɴ : 1.0.6
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪</b>"""
  
  STATUS_TXT = """<b>╔════❰ ʙᴏᴛ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼👱 ᴛᴏᴛᴀʟ ᴜsᴇʀs: {}
║┃
║┣⪼🤖 ᴛᴏᴛᴀʟ ʙᴏᴛ: {}
║┃
║┣⪼🔃 ғᴏʀᴡᴀʀᴅɪɴɢs: {}
║┃
║┣⪼🔍 ᴜɴᴇǫᴜɪꜰʏɪɴɢs: {}
║╰━━━━━━━━━━━━━━━➣
╚══════════════════❍⊱❁۪۪</b>
"""
  
  FROM_MSG = "<b>❪ SET SOURCE CHAT ❫\n\nForward the last message or last message link of source chat.\n/cancel - cancel this process</b>"
  TO_MSG = "<b>❪ CHOOSE TARGET CHAT ❫\n\nChoose your target chat from the given buttons.\n/cancel - Cancel this process</b>"
  SKIP_MSG = "<b>❪ SET MESSAGE SKIPING NUMBER ❫</b>\n\n<b>Skip the message as much as you enter the number and the rest of the message will be forwarded\nDefault Skip Number =</b> <code>0</code>\n<code>eg: You enter 0 = 0 message skiped\n You enter 5 = 5 message skiped</code>\n/cancel <b>- cancel this process</b>"
  CANCEL = "<b>Process Cancelled Succefully !</b>"
  BOT_DETAILS = "<b><u>📄 BOT DETAILS</b></u>\n\n<b>➣ NAME:</b> <code>{}</code>\n<b>➣ BOT ID:</b> <code>{}</code>\n<b>➣ USERNAME:</b> @{}"
  USER_DETAILS = "<b><u>📄 USERBOT DETAILS</b></u>\n\n<b>➣ NAME:</b> <code>{}</code>\n<b>➣ USER ID:</b> <code>{}</code>\n<b>➣ USERNAME:</b> @{}"
         
  TEXT = """<b>╔════❰ ғᴏʀᴡᴀʀᴅ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪</b>
<b>║╭━━━━━━━━━━━━━━━➣</b>
<b>║┣⪼𖨠 ғᴇᴄʜᴇᴅ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ʀᴇᴍᴀɪɴɪɴɢ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 sᴜᴄᴄᴇғᴜʟʟʏ ғᴏʀᴡᴀʀᴅᴇᴅ:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ᴅᴇʟᴇᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 sᴋɪᴘᴘᴇᴅ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┃⪼𖨠 ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ᴘᴇʀᴄᴇɴᴛᴀɢᴇ:</b> <code>{}</code> %
<b>║┃</b>
<b>║┣⪼𖨠ᴇᴛᴀ:</b> <code>{}</code>
<b>║╰━━━━━━━━━━━━━━━➣ 
╚════❰ ᴅᴇᴀᴛʜ ᴄᴏᴍᴍᴜɴɪᴛʏ ❱══❍⊱❁۪۪</b>
"""

  TEXT1 = """<b>╔════❰ ғᴏʀᴡᴀʀᴅ sᴛᴀᴛᴜs  ❱═❍⊱❁۪۪</b>
<b>║╭━━━━━━━━━━━━━━━➣</b>
<b>║┣⪼𖨠 ғᴇᴄʜᴇᴅ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ʀᴇᴍᴀɪɴɪɴɢ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 sᴜᴄᴄᴇғᴜʟʟʏ ғᴏʀᴡᴀʀᴅᴇᴅ:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ᴅᴇʟᴇᴛᴇᴅ ᴍᴇꜱꜱᴀɢᴇ:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 sᴋɪᴘᴘᴇᴅ ᴍᴇssᴀɢᴇs:</b> <code>{}</code>
<b>║┃</b>
<b>║┃⪼𖨠 ᴄᴜʀʀᴇɴᴛ sᴛᴀᴛᴜs:</b> <code>{}</code>
<b>║┃</b>
<b>║┣⪼𖨠 ᴘᴇʀᴄᴇɴᴛᴀɢᴇ:</b> <code>{}</code> %
<b>║┃</b>
<b>║┣⪼𖨠ᴇᴛᴀ:</b> <code>{}</code>
<b>║╰━━━━━━━━━━━━━━━➣ 
╚════❰ ᴅᴇᴀᴛʜ ᴄᴏᴍᴍᴜɴɪᴛʏ ❱══❍⊱❁۪۪</b>"""

  DUPLICATE_TEXT = """╔════❰ ᴜɴᴇǫᴜɪғʏ sᴛᴀᴛᴜs ❱═❍⊱❁۪۪
║╭━━━━━━━━━━━━━━━➣
║┣⪼ <b>ғᴇᴛᴄʜᴇᴅ ғɪʟᴇs:</b> <code>{}</code>
║┃
║┣⪼ <b>ᴅᴜᴘʟɪᴄᴀᴛᴇ ᴅᴇʟᴇᴛᴇᴅ:</b> <code>{}</code> 
║╰━━━━━━━━━━━━━━━➣
╚════❰ {} ❱══❍⊱❁۪۪
"""
  DOUBLE_CHECK = """<b><u>DOUBLE CHECKING ⚠️</b></u>
<code>Before forwarding the messages Click the Yes button only after checking the following</code>

<b>★ YOUR BOT:</b> [{botname}](t.me/{botuname})
<b>★ FROM CHANNEL:</b> `{from_chat}`
<b>★ TO CHANNEL:</b> `{to_chat}`
<b>★ SKIP MESSAGES:</b> `{skip}`

<i>° [{botname}](t.me/{botuname}) must be admin in **TARGET CHAT**</i> (`{to_chat}`)
<i>° If the **SOURCE CHAT** is private your userbot must be member or your bot must be admin in there also</b></i>

<b>If the above is checked then the yes button can be clicked</b>"""
