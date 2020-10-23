from swallow.templator import templates_engine


def index(request):
    secret = request.get('secret_key', None)
    static = request.get('static', None)
    return '200 OK', templates_engine('index.html', secret=secret, static=static)


def products(request):
    secret = request.get('secret_key', None)
    return '200 OK', templates_engine('products.html', secret=secret)


def contacts(request):
    secret = request.get('secret_key', None)
    return '200 OK', templates_engine('contacts.html', secret=secret)
