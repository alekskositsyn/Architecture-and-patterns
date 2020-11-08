""" Шаблонизатор. """
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def templates_engine(template_name, folder='../templates', **kwargs):
    """
    Шаблонизатор - осуществляет рендер шаблонов.
    :param template_name: имя шаблона
    :param folder: папка с шаблонами
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    # folder_path = os.path.join(folder, template_name)
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    # Пример использования
    output_test = templates_engine('contacts.html')
    print(output_test)
