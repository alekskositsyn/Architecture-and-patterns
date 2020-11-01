from swallow.templator import templates_engine


def index(request):
    secret = request.get('secret_key', None)
    static = request.get('static', None)
    return '200 OK', templates_engine('index.html', secret=secret, static=static)


def products(request):
    secret = request.get('secret_key', None)
    return '200 OK', templates_engine('products.html', secret=secret)


def contacts(request):
    if request['method'] == 'POST':
        data = request['data']
        user_name = data['user_name']
        text = data['text']
        email = data['email']
        with open('client_messages.txt', 'a') as f:
            f.write(f'Пришло сообщение от {user_name} {email} c текстом: {text} \n')
        return '200 OK', templates_engine('contacts.html')
    return '200 OK', templates_engine('contacts.html')
