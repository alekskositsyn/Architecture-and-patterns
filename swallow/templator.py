import os
from jinja2 import Template


def templates_engine(template_name, folder='templates', **kwargs):
    """
    Шаблонизатор - осуществляет рендер шаблонов.
    :param template_name: имя шаблона
    :param folder: папка с шаблонами
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    path = os.path.join(folder, template_name)
    with open(path, encoding='utf-8') as html:
        template = Template(html.read())
    return template.render(**kwargs)

