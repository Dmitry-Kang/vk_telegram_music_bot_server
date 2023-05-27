# -*- coding: utf-8 -*-
import sqlite3
import os

def getUser(vk_id):
	conn = sqlite3.connect('database.db')
	c = conn.cursor()
	c.execute(f"select * from users where vk_id = {vk_id}")
	data = c.fetchall()

	conn.commit()
	conn.close()
	if len(data) > 0:
		return {"id": data[0][0], "created_at": data[0][1], "updated_at": data[0][2], "vk_id": data[0][3], "tg_id": data[0][4]}
	return None

# Если стикеры не найдены, то добавляем их в бд
def addStickerIntoDb( stickers ):

	conn = sqlite3.connect('bot.db')
	c = conn.cursor()

	c.execute("INSERT INTO stickers VALUES ( '" + stickers[0].get('sticker_t') + "' , '" + stickers[0].get('sticker_vk') + "')")

	conn.commit()
	conn.close()

