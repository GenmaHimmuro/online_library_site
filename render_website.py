import json
from pprint import pprint
from jinja2 import Environment, FileSystemLoader, select_autoescape
from http.server import HTTPServer, SimpleHTTPRequestHandler
from livereload import Server, shell


def render_library_site():
    with open("meta_data.json", "r", encoding='UTF-8') as my_file:
        meta_data_json = my_file.read()

    books = json.loads(meta_data_json)

    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    rendered_page = template.render(books=books)

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

render_library_site()

server = Server()
server.watch('template.html', render_library_site)
server.serve(root='.')
