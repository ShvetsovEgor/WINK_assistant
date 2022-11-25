import sqlite3

con = sqlite3.connect("db_achievements.db")
cur = con.cursor()



def process_achievement(quest_id, user_id, add=1):
    prog = cur.execute(f"""SELECT prog{quest_id} FROM users WHERE id = {user_id}""").fetchone()[0]
    max_value = cur.execute(f"""SELECT max_value FROM quests_params WHERE id = {quest_id}""").fetchone()[0]
    block_id = cur.execute(f"""SELECT block_id FROM quests_params WHERE id = {quest_id}""").fetchone()[0]
    block_prog = cur.execute(f"""SELECT block_prog{block_id} FROM users WHERE id = {user_id}""").fetchone()[0]
    if prog == max_value:
        return
    prog += add
    if prog >= max_value:
        prog = max_value
        block_prog += 1

    cur.execute(f"""UPDATE users SET prog{quest_id} = {prog} WHERE id = {user_id}""")
    con.commit()
    cur.execute(f"""UPDATE users SET block_prog{block_id} = {block_prog} WHERE id = {user_id}""")
    con.commit()
    return

#   process_achievement(0, 0, 5)


