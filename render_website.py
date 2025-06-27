import json
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server, shell
from more_itertools import chunked


def render_library_site():
    with open("meta_data.json", "r", encoding='UTF-8') as my_file:
        meta_data_json = my_file.read()

    books_chunked = list(chunked(json.loads(meta_data_json),2))

    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    return template.render(books_rows=books_chunked)


def on_reload(rendered_page):
    with open('index.html', 'w', encoding="utf8") as file:
        return file.write(rendered_page)


def main():
    on_reload(render_library_site())
    server = Server()
    server.watch('template.html', render_library_site)
    server.serve(root='.')


if __name__ == '__main__':
    main()
