import sqlite3
import threading

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


class PersonMapper:
    """
    Паттерн DATA MAPPER
    Слой преобразования данных
    """

    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_person):
        statement = f"SELECT ID, FIRSTNAME, LASTNAME \
                      FROM SPORTSMAN WHERE ID='{id_person}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return Sportsman(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id_person} not found')

    def insert(self, person):
        statement = f"INSERT INTO SPORTSMAN (FIRSTNAME, LASTNAME) VALUES \
                      ('{person.first_name}', '{person.last_name}')"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, person):
        statement = f"UPDATE SPORTSMAN SET FIRSTNAME='{person.first_name}', LASTNAME='{person.last_name}' \
                      WHERE ID='{person.id_person}'"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, person):
        statement = f"DELETE FROM SPORTSMAN WHERE ID='{person.id_person}'"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_category):
        statement = f"SELECT NAME \
                         FROM CATEGORY WHERE ID='{id_category}'"
        self.cursor.execute(statement)
        result = self.cursor.fetchall()
        if result:
            return Category(*result[0])
        else:
            raise RecordNotFoundException(f'record with id={id_category} not found')

    def insert(self, category):
        statement = f"INSERT INTO CATEGORY (NAME) VALUES \
                         ('{category.name}')"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, category):
        statement = f"UPDATE CATEGORY SET NAME='{category.name}' \
                         WHERE ID='{category.id_category}'"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, category):
        statement = f"DELETE FROM CATEGORY WHERE ID='{category.id_category}'"
        self.cursor.execute(statement)
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Sportsman):
            return PersonMapper(connection)
        if isinstance(obj, Category):
            return CategoryMapper(connection)


class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """
    # Работает с конкретным потоком
    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Sportsman(DomainObject):
    def __init__(self, id_person, first_name, last_name):
        self.id_person = id_person
        self.last_name = last_name
        self.first_name = first_name


class Category(DomainObject):
    def __init__(self, id_category, name):
        self.id_category = id_category
        self.name = name


try:
    UnitOfWork.new_current()
    new_person_1 = Sportsman('1', 'Igor', 'Igorev')
    new_person_1.mark_new()

    new_person_2 = Sportsman('2', 'Fedor', 'Fedorov')
    new_person_2.mark_new()

    new_category = Category(None, 'Rifle')
    new_category.mark_new()

    new_category = Category(None, 'Pistol')
    new_category.mark_new()
    person_mapper = PersonMapper(connection)
    exists_person_1 = person_mapper.find_by_id(1)
    exists_person_1.mark_dirty()
    print(exists_person_1.first_name)
    exists_person_1.first_name += ' Senior'
    print(exists_person_1.first_name)

    exists_person_2 = person_mapper.find_by_id(2)
    exists_person_2.mark_removed()

    print(UnitOfWork.get_current().__dict__)

    UnitOfWork.get_current().commit()
except Exception as e:
    print(e.args)
finally:
    UnitOfWork.set_current(None)

print(UnitOfWork.get_current())
