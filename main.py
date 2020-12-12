import os

from mappers import MapperRegistry
from swallow.my_wsgi import Application, DebugModeApplication, FakeApplication
from logging_model import Logger, debug
from models import TrainingPage, BaseSerializer, EmailNotifier, SmsNotifier
from swallow.templator import templates_engine
from swallow.swallow_cbv import ListView, CreateView

# Fronts Controllers
from swallow_orm.unitofwork import UnitOfWork


def secret_fc(request):
    request['secret_key'] = 'some secret'


def do_static(request):
    path = os.path.join('static', 'style.css')
    request['static'] = path


front_controllers = [secret_fc, do_static]
site = TrainingPage()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


@debug
def index(request):
    secret = request.get('secret_key', None)
    static = request.get('static', None)
    return '200 OK', templates_engine('index.html')


class GroupCreateView(CreateView):
    template_name = 'create_group.html'

    def create_obj(self, data: dict):
        type_ = data['group_type']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_group = site.create_group(type_, category)
        site.categories.append(new_group)
        new_group.mark_new()
        UnitOfWork.get_current().commit()


# @debug
# def create_group(request):
#     if request['method'] == 'POST':
#         # метод пост
#         data = request['data']
#         name = data['name']
#         # group_type = data['group_type']
#         category_id = data.get('category_id')
#         print(category_id)
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#             course = site.create_group('start', name, category)
#             site.groups.append(course)
#         # редирект?
#         # return '302 Moved Temporarily', templates_engine('group_list.html')
#         # Для начала можно без него
#         return '200 OK', templates_engine('create_group.html')
#     else:
#         # groups = site.groups
#         categories = site.categories
#         return '200 OK', templates_engine('create_group.html', categories=categories)


class CategoryCreateView(CreateView):
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['groups'] = site.groups
        return context

    def create_obj(self, data: dict):
        name = data['name']
        # category_id = data.get('category_id')
        # category = None
        # if category_id:
        #     category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name)
        site.categories.append(new_category)
        new_category.mark_new()
        UnitOfWork.get_current().commit()


# def create_category(request):
#     if request['method'] == 'POST':
#         # метод пост
#         data = request['data']
#         # print(data)
#         name = data['name']
#         category_id = data.get('category_id')
#
#         category = None
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#         # редирект?
#         return '302 Moved Temporarily', templates_engine('create_group.html')
#         # Для начала можно без него
#         # return '200 OK', templates_engine('create_category.html')
#     else:
#         categories = site.categories
#         return '200 OK', templates_engine('create_category.html', categories=categories)
class CategoryListView(ListView):
    # queryset = site.categories
    template_name = 'category_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('category')
        return mapper.all()


class SportsmanListView(ListView):
    # queryset = site.sportsman
    template_name = 'sportsman_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('sportsman')
        return mapper.all()


class SportsmanCreateView(CreateView):
    template_name = 'create_sportsman.html'

    def create_obj(self, data: dict):
        firstname = data['firstname']
        lastname = data['lastname']
        new_obj = site.create_user('sportsman', firstname, lastname)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


class AddSportsmanByGroupCreateView(CreateView):
    template_name = 'add_sportsman.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['groups'] = site.groups
        context['sportsman'] = site.sportsman
        return context

    def create_obj(self, data: dict):
        group_name = data['group_name']
        group = site.get_group(group_name)
        sportsman_name = data['sportsman_name']
        sportsman = site.get_student(sportsman_name)
        group.add_sportsman(sportsman)


# @debug
# def add_user(request):
#     if request['method'] == 'POST':
#         data = request['data']
#         print(data)
#         user_type = data['user_type']
#         first_name = data['first_name']
#         second_name = data['second_name']
#         age = data['age']
#         email = data['email']
#         phone = data['phone']
#         print(user_type)
#         with open('base_client.txt', 'a') as f:
#             f.write(f'Запись в группу {user_type} '
#                     f'{first_name} '
#                     f'{second_name}  '
#                     f'{second_name} '
#                     f'{email} '
#                     f'{age} '
#                     f'{phone} \n')
#         return '200 OK', templates_engine('add_user.html')
#     return '200 OK', templates_engine('add_user.html')


urls = {
    '/': index,
    '/create-group/': GroupCreateView(),
    '/create-category/': CategoryCreateView(),
    '/category-list/': CategoryListView(),
    '/sportsman-list/': SportsmanListView(),
    '/create-sportsman/': SportsmanCreateView(),
    '/add-sportsman/': AddSportsmanByGroupCreateView(),
}

# application = Application(urls, front_controllers)
application = DebugModeApplication(urls, front_controllers)


# application = FakeApplication(urls, front_controllers)


@application.add_urls('/copy-group/')
@debug
def copy_course(request):
    request_params = request['request_params']
    # print(request_params)
    name = request_params['name']
    old_group = site.get_group(name)
    if old_group:
        new_name = f'copy_{name}'
        new_group = old_group.clone()
        new_group.name = new_name
        site.groups.append(new_group)

    return '200 OK', templates_engine('group_list.html', objects_list=site.groups)


# @application.add_urls('/category-list/')
# @debug
# def category_list(request):
#     logger.log('List categories')
#     return '200 OK', templates_engine('category_list.html', objects_list=site.categories)
#
#
@application.add_urls('/group-list/')
@debug
def group_list(request):
    logger.log('List groups')
    return '200 OK', templates_engine('group_list.html', objects_list=site.categories)


@application.add_urls('/api/')
def course_api(request):
    return '200 OK', BaseSerializer(site.groups).save()
