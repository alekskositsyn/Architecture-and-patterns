class Application:
    """
    Класс - приложение обработчик запросов клиента
    """

    def add_urls(self, urls):
        """ Декоратор (структурный патерн) """

        def inner(view):
            self.urls[urls] = view

        return inner

    def create_data_dict(self, data: str):
        """ Функция создает словарь с данными. """
        result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                result[key] = value
        return result

    def wsgi_decode_input_data(self, data: bytes):
        """
        Функция принимает данные в байтах,
        декодирует их и возвращает их в словаре.
        """
        result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            result = self.create_data_dict(data_str)
        return result

    def get_wsgi_input_data(self, env):
        """ Функция возвращает данные, если они есть в запросе. """
        content_length_data = env.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = env['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def __init__(self, urls, front_controllers):
        self.urls = urls
        self.front_controllers = front_controllers

    def __call__(self, environ, first_response):
        """
        :param environ: словарь данных от сервера
        :param first_response: функция для ответа серверу
        """
        path = environ['PATH_INFO']
        # добавление закрывающего слеша, если его нет
        if not path.endswith('/'):
            path = f'{path}/'

        request_method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.wsgi_decode_input_data(data)
        query_string = environ['QUERY_STRING']
        request_params = self.create_data_dict(query_string)

        if path in self.urls:
            view = self.urls[path]
            request = {
                'method': request_method,
                'data': data,
                'request_params': request_params
            }

            for front in self.front_controllers:
                front(request)
            code, body = view(request)
            first_response(code, [('Content-Type', 'text/html')])
            return [body.encode('utf-8')]
        else:
            first_response('404 Not Found', [('Content-Type', 'text/html')])
            return [b'Not Found']


class DebugModeApplication(Application):
    def __init__(self, urls, front_controllers):
        self.application = Application(urls, front_controllers)
        super().__init__(urls, front_controllers)

    def __call__(self, environ, first_response):
        print('DEBUG MODE')
        # print(environ)
        return super().__call__(environ, first_response)
        # return self.application(environ, first_response)



    def add_urls(self, urls):
        """ Декоратор (структурный патерн) """

        def inner(view):
            self.urls[urls] = view

        return inner
