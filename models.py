from reusepatterns.prototypes import PrototypeMixin


class User:
    pass


class Trainer(User):
    pass


class Sportsman(User):
    pass


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
        self.groups = []

    def group_count(self):
        result = len(self.groups)
        if self.category:
            result += self.category.group_count()
        return result


class Group(PrototypeMixin):

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.groups.append(self)


class InteractiveCourse(Group):
    pass


class RecordCourse(Group):
    pass


class GroupFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingPage:
    # Интерфейс
    def __init__(self):
        self.teachers = []
        self.students = []
        self.groups = []
        self.categories = []

    def create_user(self, type_):
        return UserFactory.create(type_)

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

    def create_groupe(self, type_, name, category):
        return GroupFactory.create(type_, name, category)

    def get_group(self, name) -> Group:
        for item in self.groups:
            if item.name == name:
                return item
        return None
