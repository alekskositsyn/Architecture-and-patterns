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


front_controllers = [secret_fc, do_static]

application = Application(ways, front_controllers)
