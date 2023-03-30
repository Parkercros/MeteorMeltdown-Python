import sqlite3

CONN = sqlite3.connect('high_scores.db')
CURSOR = CONN.cursor()


conn = sqlite3.connect('player.db')
c = conn.cursor()

c.execute('''
CREATE TABLE IF NOT EXISTS player (
    id INTEGER PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()

class Player:
    @staticmethod
    def create(name):
        try:
            c.execute("INSERT INTO player (name) VALUES (?)", (name,))
            conn.commit()
        except sqlite3.IntegrityError:
            # Player with the same name already exists
            pass

    @staticmethod
    def get_all():
        c.execute("SELECT * FROM player")
        return c.fetchall()


class HighScore:

    def __init__(self, player_name, score, id=None):
        self.id = id
        self.player_name = player_name
        self.score = score

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS high_scores
                (id INTEGER PRIMARY KEY,
                player_name TEXT,
                score INTEGER)
        """

        CURSOR.execute(sql)

    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS high_scores
        """

        CURSOR.execute(sql)

    def save(self):
        sql = """
            INSERT INTO high_scores (player_name, score)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.player_name, self.score))
        self.id = CURSOR.lastrowid
        CONN.commit()
        
    @classmethod
    def create(cls, player_name, score):
        high_score = cls(player_name, score)
        high_score.save()
        return high_score

    @classmethod
    def new_from_db(cls, row):
        high_score = cls(
            player_name=row[1],
            score=row[2],
            id=row[0]
        )

        return high_score

    @classmethod
    def get_top_scores(cls, limit=10):
        sql = """
            SELECT * FROM high_scores
            ORDER BY score DESC
            LIMIT ?
        """

        return [cls.new_from_db(row) for row in CURSOR.execute(sql, (limit,)).fetchall()]

    @classmethod
    def find_by_id(cls, id):
        sql = """
            SELECT * FROM high_scores
            WHERE id = ?
            LIMIT 1
        """

        row = CURSOR.execute(sql, (id,)).fetchone()
        if not row:
            return None

        return HighScore(
            player_name=row[1],
            score=row[2],
            id=row[0]
        )

    def update(self):
        sql = """
            UPDATE high_scores
            SET player_name = ?,
                score = ?
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.player_name, self.score, self.id))

    @classmethod
    def delete(cls, id):
        sql = """
            DELETE FROM high_scores
            WHERE id = ?
        """

        CURSOR.execute(sql, (id,))
