import os
from swallow.my_wsgi import Application, DebugModeApplication, FakeApplication
from logging_model import Logger, debug
from models import TrainingPage
from swallow.templator import templates_engine


# Fronts Controllers
def secret_fc(request):
    request['secret_key'] = 'some secret'


def do_static(request):
    path = os.path.join('static', 'style.css')
    request['static'] = path


front_controllers = [secret_fc, do_static]
site = TrainingPage()
logger = Logger('main')


@debug
def index(request):
    secret = request.get('secret_key', None)
    static = request.get('static', None)
    return '200 OK', templates_engine('index.html')


@debug
def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        # print(data)
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        category = None
        if category_id:
            group = site.find_category_by_id(category_id)

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', templates_engine('create_category.html')
    else:
        groups = site.groups
        return '200 OK', templates_engine('create_category.html', groups=groups)


@debug
def create_group(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        print(data)
        name = data['name']
        group_id = data.get('group_id')
        print(group_id)
        group = None
        if group_id:
            group = site.find_category_by_id(group_id)

            group = site.create_group('start', name, group)
            site.categories.append(group)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', templates_engine('create_group.html')
    else:
        groups = site.groups
        print(groups)
        return '200 OK', templates_engine('create_group.html', groups=groups)


@debug
def add_user(request):
    if request['method'] == 'POST':
        data = request['data']
        print(data)
        user_type = data['user_type']
        first_name = data['first_name']
        second_name = data['second_name']
        age = data['age']
        email = data['email']
        phone = data['phone']
        print(user_type)
        with open('base_client.txt', 'a') as f:
            f.write(f'Запись в группу {user_type} '
                    f'{first_name} '
                    f'{second_name}  '
                    f'{second_name} '
                    f'{email} '
                    f'{age} '
                    f'{phone} \n')
        return '200 OK', templates_engine('add_user.html')
    return '200 OK', templates_engine('add_user.html')


urls = {
    '/': index,
    '/create-group/': create_group,
    '/create-category/': create_category,
    '/add-user/': add_user
}
# application = Application(urls, front_controllers)
# application = DebugModeApplication(urls, front_controllers)
application = FakeApplication(urls, front_controllers)


@application.add_urls('/copy-group/')
@debug
def copy_group(request):
    request_params = request['request_params']
    print(request_params)
    name = request_params['name']
    old_group = site.get_group(name)
    if old_group:
        new_name = f'copy_{name}'
        new_course = old_group.clone()
        new_course.name = new_name
        site.categories.append(new_course)
    return '200 OK', templates_engine('group_list.html', objects_list=site.categories)


@application.add_urls('/category-list/')
@debug
def category_list(request):
    logger.log('List categories')
    return '200 OK', templates_engine('category_list.html', objects_list=site.categories)


@application.add_urls('/group-list/')
@debug
def group_list(request):
    logger.log('List groups')
    return '200 OK', templates_engine('group_list.html', objects_list=site.groups)
