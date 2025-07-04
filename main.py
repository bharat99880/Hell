import re
import asyncio
import random
from collections import defaultdict
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from telethon.tl.functions.account import UpdateStatusRequest  # ✅ Correct import for online

# ✅ Your credentials
API_ID = 26800922
API_HASH = "7afe6263d7cf10c8b0a984a38f94ac11"
SESSION_STRING = "1BVtsOJABu16Gfjsic_uMaJWli4TLbd4RpHikm2aLcXwsD1P6bMfxDJ8myo1ZcWlVXioX7q1vxhEEYYAAJ_EWh7SKP651tvLBsmLo8XycY73bkELXGzXhGFPHfkIv_YzA9hGRZhF_B1UkMjRT-4b4ccf3FdEA94bhDOaQqUSF19XmJaHrQgPyqrW41XZF0XG3q1nO7evPnv2rUlil_Ajzx98CghEI7D28nMkwgaj4D0Aab4u0vmiG0_HxFbFK5ubRYxXG_dSMKgSS55GIN_75M41fcmQ0lcG87af95i6q6fUTw_PNS7YhgLDfeHzYbz37jB--U31aS25535aEJ_htfbjVzqP-P-g="
OWNER_ID = 7043216350
CHEAT_BOT = 6355945378  # @collect_waifu_cheats_bot

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

# ✅ Always Online Function
async def stay_online():
    while True:
        try:
            await client(UpdateStatusRequest(offline=False))
        except Exception as e:
            print(f"[❌ StayOnline Error] {e}")
        await asyncio.sleep(60)

# Load gali.txt
with open("gali.txt", encoding="utf-8") as f:
    GALIS = [line.strip() for line in f if line.strip()]

# Load triggers
with open("triggers.txt", encoding="utf-8") as f:
    TRIGGERS = [line.strip() for line in f if line.strip()]

# ✅ States
auto_grab = True
last_group_id = {}
raid_targets = defaultdict(lambda: {"chat": None, "galis": [], "count": 0})

# ────────────── SPAM FEATURE ──────────────
@client.on(events.NewMessage(pattern=r".spam\s+(\d+)\s+(.+)", from_users=OWNER_ID))
async def reply_spam(event):
    reply = await event.get_reply_message()
    if not reply:
        return await event.reply("❌ Reply to someone's message with .spam 10 hello")
    count = int(event.pattern_match.group(1))  
    msg = event.pattern_match.group(2)  
    try: await event.delete()
    except: pass
    for _ in range(count):  
        await client.send_message(event.chat_id, msg, reply_to=reply.id)

# ────────────── RAID FEATURE ──────────────
@client.on(events.NewMessage(pattern=r".raid\s+(\d+)", from_users=OWNER_ID))
async def raid_cmd(event):
    reply_msg = await event.get_reply_message()
    if not reply_msg:
        return await event.reply("❌ Reply to someone's message to raid!")
    try: await event.delete()
    except: pass
    count = int(event.pattern_match.group(1))  
    target_id = reply_msg.sender_id  
    chat_id = event.chat_id  
    total_galis_needed = count * 30  
    galis = random.sample(GALIS * ((total_galis_needed // len(GALIS)) + 1), total_galis_needed)  
    raid_targets[target_id] = {"chat": chat_id, "galis": galis, "count": count}

@client.on(events.NewMessage())
async def handle_auto_reply(event):
    user_id = event.sender_id
    chat_id = event.chat_id
    if user_id in raid_targets:  
        data = raid_targets[user_id]  
        if chat_id == data["chat"] and data["count"] > 0:  
            data["count"] -= 1  
            for _ in range(30):  
                if data["galis"]:  
                    gali = data["galis"].pop(0)  
                    try:  
                        await client.send_message(chat_id, gali, reply_to=event.id)  
                        await asyncio.sleep(0.7)
                    except: pass
            if data["count"] <= 0 or not data["galis"]:  
                raid_targets.pop(user_id, None)

@client.on(events.NewMessage(pattern=r"/stopraid", from_users=OWNER_ID))
async def stop_raid(event):
    raid_targets.clear()
    await event.reply("Raid stopped.")

# ────────────── PROFILE INFO ──────────────
@client.on(events.NewMessage(pattern=r".dinfo", from_users=OWNER_ID))
async def info(event):
    me = await client.get_me()
    try:
        await client.send_file(
            event.chat_id,
            "pfp.jpg",
            caption=f"""🎭 𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗦𝘁𝗮𝘁𝘂𝘀 — 𝗟𝗘𝗚𝗘𝗡𝗗𝗔𝗥𝗬 ☠️

╭──────────────────────╮
┃ 👤 𝗡𝗮𝗺𝗲: {me.first_name}
┃ 🆔 𝗨𝘀𝗲𝗿 𝗜𝗗: {me.id}
┃ 🌐 𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{me.username if me.username else "N/A"}
┃ 🧠 𝗕𝗶𝗼: THAT’S RIGHT I AM KIRA
┃ ⚡ 𝗦𝘁𝗮𝘁𝘂𝘀: 𝗔𝗖𝗧𝗜𝗩𝗘 ✅
┃ 🔥 𝗕𝗲𝘁𝗮 𝗕𝘂𝗶𝗹𝗱 — 𝗗𝗘𝗩: 𝗞𝗜𝗥𝗔
╰──────────────────────╯
""")
    except:
        await event.reply("❌ pfp.jpg not found!")

# ────────────── AUTO GRAB WAIFU ──────────────
WAIFU_HUSBANDO_BOT_IDS = [6195436879, 6546492683]
WAIFU_HUSBANDO_BOT_USERNAMES = ["Waifu_Grabber_Bot", "Husbando_Grabber_Bot"]

@client.on(events.NewMessage(pattern="/xon", from_users=OWNER_ID))
async def turn_on(event):
    global auto_grab
    auto_grab = True
    await event.reply("Auto Grab is ON")

@client.on(events.NewMessage(pattern="/xoff", from_users=OWNER_ID))
async def turn_off(event):
    global auto_grab
    auto_grab = False
    await event.reply("Auto Grab is OFF")

@client.on(events.NewMessage(incoming=True))
async def detect_waifu(event):
    if not auto_grab:
        return
    sender = await event.get_sender()  
    sender_id = event.sender_id  
    sender_username = sender.username if sender else None  
    if sender_id not in WAIFU_HUSBANDO_BOT_IDS and (sender_username not in WAIFU_HUSBANDO_BOT_USERNAMES):  
        return
    for trigger in TRIGGERS:  
        if trigger.lower() in event.raw_text.lower():  
            try:  
                fwd_msg = await client.forward_messages(CHEAT_BOT, event.message)  
                last_group_id[fwd_msg.id] = event.chat_id  
            except Exception as e:  
                print(f"❌ Forward failed: {e}")  
            break

@client.on(events.NewMessage(from_users=CHEAT_BOT))
async def reply_from_cheat_bot(event):
    text = event.raw_text
    match = re.search(r"Humanizer:\s*/grab\s+([a-zA-Z]+)", text)
    if not match:
        return
    first_name = match.group(1).lower()  
    reply_msg = await event.get_reply_message()  
    if not reply_msg or reply_msg.id not in last_group_id:  
        return
    group_id = last_group_id[reply_msg.id]  
    try:  
        delay = random.uniform(2.2, 2.4)  
        await asyncio.sleep(delay)  
        sent_msg = await client.send_message(group_id, f"/grab {first_name}")  
        print(f"✅ Grabbed: /grab {first_name} in group {group_id}")  
        await asyncio.sleep(30)  
        await client.delete_messages(group_id, sent_msg)
    except Exception as e:  
        print(f"❌ Grab error: {e}")

@client.on(events.NewMessage(pattern="/startgrab", from_users=OWNER_ID))
async def manual_start(event):
    try:
        await client.send_message(CHEAT_BOT, "/start")
        await event.reply("✅ Sent /start to cheat bot")
    except Exception as e:
        await event.reply(f"❌ Failed: {e}")

# ✅ Main function — starts bot and stay_online loop
async def main():
    await client.start()
    client.loop.create_task(stay_online())  # ✅ Always Online
    print("🔥 KIRA Combined Userbot is running... [Online Mode Enabled]")
    await client.run_until_disconnected()

client.loop.run_until_complete(main())