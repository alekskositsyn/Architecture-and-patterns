import os
import views
from swallow.my_wsgi import Application

ways = {
    '/': views.index,
    '/products/': views.products,
    '/contacts/': views.contacts
}


# Fronts Controllers
def secret_fc(request):
    request['secret_key'] = 'some secret'


def do_static(request):

    path = os.path.join('static', 'style.css')
    request['static'] = path


def path_validator(path):
    """
    Добавляет в конце пути '/' при его отсутствии.
    :param path: путь
    :return:
    """
    last_symbol = path[-1:]
    if last_symbol != '/':
        return path + '/'
    return path


front_controllers = [secret_fc, do_static]

application = Application(ways, front_controllers, path_validator)
