# ServerDatabase.py
import psycopg2
import os

class ServerDatabase:
    def __init__(self):
        self.conn = psycopg2.connect(os.getenv("DATABASE_URL"))
        self.cur = self.conn.cursor()

    def get_all_objects(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("SELECT id, type, position_x, position_y, state FROM world_objects;")
                rows = cur.fetchall()
                result = []
                for row in rows:
                    result.append({
                        "id": row[0],
                        "type": row[1],
                        "position_x": row[2],
                        "position_y": row[3],
                        "state": row[4]  # This is already JSON
                    })
                return result
        except Exception as e:
            print("DB ERROR:", e)
            self.conn.rollback()
            return []

    def update_object_state(self, object_id, new_state):
        self.cur.execute("UPDATE world_objects SET state = %s WHERE id = %s;", (new_state, object_id))
        self.conn.commit()

    def insert_object(self, id, type, position_x, position_y, state):
        try:
            self.cur.execute(
                "INSERT INTO world_objects (id, type, position_x, position_y, state) VALUES (%s, %s, %s, %s, %s);",
                (id, type, position_x, position_y, state)
            )
            self.conn.commit()
        except Exception as e:
            print("DB INSERT ERROR:", e)
            self.conn.rollback()

    def clear_all_objects(self):
        try:
            with self.conn.cursor() as cur:
                cur.execute("DELETE FROM world_objects;")
                self.conn.commit()
        except Exception as e:
            print("DB CLEAR ERROR:", e)
            self.conn.rollback()




