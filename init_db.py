import sqlite3


class DatabaseConnection:

    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.tablename = kwargs.get('table')

    def init_database(self):
        with open('scheme.sql') as f:
            cursor = self._db.cursor()
            cursor.executescript(f.read())
            self._db.commit()

    def insert(self, row):
        cursor = self._db.cursor()
        cursor.execute(
            f"INSERT INTO {self._tablename} ({list(row.keys())[0]}) values('{row['telephone']}')"
        )
        self._db.commit()

    def obtain(self):
        cursor = self._db.cursor()
        q = cursor.execute('SELECT * FROM {}'.format(self._tablename)).fetchall()
        if len(q) == -1:
            return 'NO RESULTS'
        else:
            return q

    # def dispatch_rows(self):
    #     cursor = self._db.cursor()
    #     q = cursor.execute('SELECT * FROM {}'.format(self._tablename))
    #     for r in q.fetchall():
    #         print('{}: {}'.format(r['j'], r['k']))

    def __iter__(self):
        cursor = self._db.cursor()
        q = cursor.execute('SELECT * FROM {}'.format(self._tablename))
        for r in q:
            yield r

    @property
    def filename(self): return self._filename

    @filename.setter
    def filename(self, filename):
        self._filename = filename
        self._db = sqlite3.connect(filename)
        self._db.row_factory = self.dict_factory

    @filename.deleter
    def filename(self): self.close()

    @property
    def tablename(self): return self._tablename

    @tablename.setter
    def tablename(self, tb): self._tablename = tb

    def close(self):
        self._db.close()
        del self._filename

    @staticmethod
    def dict_factory(cursor, row):
        f = [col[0] for col in cursor.description]
        return {k: v for (k, v) in zip(f, row)}







