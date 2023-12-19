import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()


class Dog:
    def __init__(self, name, breed):
        self.id = None  
        self.name = name
        self.breed = breed

    @classmethod
    def create_table(cls):
        cls.CURSOR.execute('''
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        ''')
        cls.CONN.commit()

    @classmethod
    def drop_table(cls):
        cls.CURSOR.execute('DROP TABLE IF EXISTS dogs')
        cls.CONN.commit()

    def save(self):
        if self.id is None:
            self.CURSOR.execute('''
                INSERT INTO dogs (name, breed) VALUES (?, ?)
            ''', (self.name, self.breed))
            self.id = self.CURSOR.lastrowid
        else:
            self.CURSOR.execute('''
                UPDATE dogs SET name=?, breed=? WHERE id=?
            ''', (self.name, self.breed, self.id))
        self.CONN.commit()

    @classmethod
    def create(cls, name, breed):
        dog = cls(name, breed)
        dog.save()
        return dog

    @classmethod
    def new_from_db(cls, data):
        dog = cls(data[1], data[2])
        dog.id = data[0]
        return dog

    @classmethod
    def get_all(cls):
        cls.CURSOR.execute('SELECT * FROM dogs')
        data = cls.CURSOR.fetchall()
        return [cls.new_from_db(row) for row in data]

    @classmethod
    def find_by_name(cls, name):
        cls.CURSOR.execute('SELECT * FROM dogs WHERE name=?', (name,))
        data = cls.CURSOR.fetchone()
        return cls.new_from_db(data) if data else None

    @classmethod
    def find_by_id(cls, dog_id):
        cls.CURSOR.execute('SELECT * FROM dogs WHERE id=?', (dog_id,))
        data = cls.CURSOR.fetchone()
        return cls.new_from_db(data) if data else None

