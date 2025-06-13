# ServerDatabase.py
import psycopg2
import os

class ServerDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cur = self.conn.cursor()

    def get_all_objects(self):
        self.cur.execute("SELECT * FROM world_objects;")
        return self.cur.fetchall()

    def update_object_state(self, object_id, new_state):
        self.cur.execute("UPDATE world_objects SET state = %s WHERE id = %s;", (new_state, object_id))
        self.conn.commit()

    def insert_object(self, id, type, position_x, position_y, state):
        self.cur.execute("INSERT INTO world_objects (id, type, position_x, position_y, state) VALUES (%s, %s, %s, %s, %s);", (id, type, position_x, position_y, state))
        self.conn.commit()

