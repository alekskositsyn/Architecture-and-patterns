import abc
from reusepatterns.prototypes import PrototypeMixin


class User:
    pass


class Trainer(User):
    pass


class Sportsman(User):
    pass


class UserCreate:
    types = {
        'trainer': Trainer,
        'sportsman': Sportsman
    }

    @classmethod
    def create(cls, type_):
        return cls.types[type_]()


class Category:
    # реестр?
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Group(PrototypeMixin):
    """ Класс для копирования групп """
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.groups.append(self)


class Start(Group):
    pass


class Medium(Group):
    pass


class Professional(Group):
    pass


class GroupFactory:
    """
    Класс фабрика групп начальной,
    средней и профессиональной подготовки
    """
    types = {
        'start': Start,
        'medium': Medium,
        'professional': Professional,
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingPage:
    # Интерфейс
    def __init__(self):
        self.trainers = []
        self.sportsman = []
        self.groups = []
        self.categories = []

    def create_user(self, type_):
        return UserCreate.create(type_)

    def create_category(self, name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            print('item', item.id)
            if item.id == id:
                return item
        raise Exception(f'Нет категории с id = {id}')

    #
    # def get_or_create_category(self, name):
    #     for item in self.categories:
    #         if item.name == name:
    #             return item
    #     return self.create_category(name)

    def create_group(self, type_, name, category):
        return GroupFactory.create(type_, name, category)

    def get_group(self, name) -> Group:
        for item in self.groups:
            if item.name == name:
                return item
        return None
