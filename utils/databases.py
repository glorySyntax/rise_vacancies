import aiosqlite

class Database:
    def __init__(self):
        self.path = 'data/database.db'

    async def create_table(self):
        async with aiosqlite.connect(self.path) as con:
            c = await con.cursor()
            await c.execute('''CREATE TABLE IF NOT EXISTS chats(
                            id INTEGER PRIMARY KEY
                            )''')
            await c.execute('''CREATE TABLE IF NOT EXISTS notifications(
                            id INTEGER PRIMARY KEY,
                            active INTEGER
            )''')
            await con.commit()

    async def add_chats(self, message: str):
        ids = message.split('\n')
        async with aiosqlite.connect(self.path) as con:
            c = await con.cursor()
            for id in ids:
                await c.execute('INSERT INTO chats VALUES(?)',(id,))
            await con.commit()

    async def add_admins(self, message: str):
        ids = message.split('\n')
        n = 0
        async with aiosqlite.connect(self.path) as con:
            c = await con.cursor()
            for id in ids:
                await c.execute('INSERT INTO notifications VALUES(?, ?)',(id, 0,))
                n += 1
            await con.commit()
        return ids

    async def set_active_admin(self, id: int):
        async with aiosqlite.connect(self.path) as con:
            c = await con.cursor()
            await c.execute('UPDATE notifications SET active =? WHERE id =?',(1, id,))
            await con.commit()