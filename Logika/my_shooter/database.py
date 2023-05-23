import sqlite3 as sq

if __name__ != '__main__':
    with sq.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS records (
                        id INTEGER PRIMARY KEY,
                        value INTEGER DEFAULT 0
                        )""")

        cur.execute("""CREATE TABLE IF NOT EXISTS profile (
                                coins INTEGER DEFAULT 0,
                                current_weapon TEXT DEFAULT "default"
                                )""")


def add_result(result):
    with sq.connect('database.db') as con:
        cur = con.cursor()
        cur.execute(f"""INSERT INTO records (value) VALUES ({result})""")


def get_record():
    with sq.connect('database.db') as con:
        cur = con.cursor()
        records = cur.execute("""SELECT value FROM records""").fetchall()

    hight_record = 0
    for record in records:
        if record[0] > hight_record:
            hight_record = record[0]
    return hight_record


def game_id():
    with sq.connect('database.db') as con:
        cur = con.cursor()
        number = cur.execute("""SELECT id FROM records""").fetchall()[-1][0]
        return number


def update_balance(money):
    with sq.connect('database.db') as con:
        cur = con.cursor()
        try:
            coins = cur.execute("""SELECT coins FROM profile""").fetchone()[0] + money
        except TypeError:
            cur.execute("""INSERT INTO profile DEFAULT VALUES""")
            coins = money

        cur.execute(f"""UPDATE profile SET coins = {coins}""")


def get_balance():
    with sq.connect('database.db') as con:
        cur = con.cursor()
        try:
            balance = cur.execute("""SELECT coins FROM profile""").fetchone()[0]
        except TypeError:
            cur.execute("""INSERT INTO profile DEFAULT VALUES""")
            balance = 0
        return balance
