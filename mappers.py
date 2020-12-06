import sqlite3
from models import Sportsman

connection = sqlite3.connect('swallow.sqlite')


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')


class SportsmanMapper:

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()
        self.table_name = 'sportsman'

    def all(self):
        statement = f'SELECT * from {self.table_name}'
        self.cursor.execute(statement)
        result = []
        for item in self.cursor.fetchall():
            id, firstname, lastname = item
            student = Sportsman(firstname, lastname)
            student.id = id
            result.append(student)
        return result

    def find_by_id(self, id):
        statement = f"SELECT id, firstname, lastname FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (id,))
        result = self.cursor.fetchone()
        if result:
            return Sportsman(*result)
        else:
            raise RecordNotFoundException(f'record with id={id} not found')

    def insert(self, obj):
        statement = f"INSERT INTO {self.table_name} (firstname, lastname) VALUES ('{obj.firstname}', '{obj.lastname}')"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, obj):
        statement = f"UPDATE {self.table_name} SET firstname=?, lastname=? WHERE id=?"
        # Где взять obj.id? Добавить в DomainModel? Или добавить когда берем объект из базы
        self.cursor.execute(statement, (obj.firstname, obj.lastname, obj.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, obj):
        statement = f"DELETE FROM {self.table_name} WHERE id=?"
        self.cursor.execute(statement, (obj.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    mappers = {
        'sportsman': SportsmanMapper
    }

    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Sportsman):
            return SportsmanMapper(connection)

    @staticmethod
    def get_current_mapper(name):
        return MapperRegistry.mappers[name](connection)
