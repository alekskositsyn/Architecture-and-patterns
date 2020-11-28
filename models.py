import jsonpickle

from reusepatterns.prototypes import PrototypeMixin
from reusepatterns.observer import Subject, Observer


class User:
    def __init__(self, name):
        self.name = name


class Trainer(User):
    pass


class Sportsman(User):
    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class SimpleFactory:
    # Фабричный метод
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'sportsman': Sportsman,
        'trainer': Trainer
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class Category:
    # реестр?
    auto_id = 0

    def __getitem__(self, item):
        return self.groups[item]

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.groups = []

    def group_count(self):
        result = len(self.groups)
        if self.category:
            result += self.category.group_count()
        return result


class Group(PrototypeMixin, Subject):
    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.groups.append(self)
        self.sportsman = []
        super().__init__()

    def __getitem__(self, item):
        return self.sportsman[item]

    def add_student(self, sportsman: Sportsman):
        self.sportsman.append(sportsman)
        sportsman.courses.append(self)
        self.notify()


class StartGroup(Group):
    pass


class MediumGroup(Group):
    pass


class ProGroup(Group):
    pass


class GroupFactory:
    types = {
        'start': StartGroup,
        'medium': MediumGroup,
        'pro': ProGroup
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class SmsNotifier(Observer):

    def update(self, subject: Group):
        print('SMS->', 'к нам присоединился', subject.sportsman[-1].name)


class EmailNotifier(Observer):

    def update(self, subject: Group):
        print(('EMAIL->', 'к нам присоединился', subject.sportsman[-1].name))


class BaseSerializer:

    def __init__(self, obj):
        self.obj = obj

    def save(self):
        return jsonpickle.dumps(self.obj)

    def load(self, data):
        return jsonpickle.loads(data)


class TrainingPage:
    # Интерфейс
    def __init__(self):
        self.teachers = []
        self.sportsman = []
        self.groups = []
        self.categories = []

    def create_user(self, type_, name):
        return UserFactory.create(type_, name)

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

    def get_student(self, name) -> Sportsman:
        for item in self.sportsman:
            if item.name == name:
                return item
