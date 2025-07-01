import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from livereload import Server
from more_itertools import chunked
from dotenv import load_dotenv
from functools import partial


def render_library_site(books_chunk, current_page, pages_count):
    env = Environment(loader=FileSystemLoader('.'), autoescape=select_autoescape(['html', 'xml']))
    template = env.get_template('template.html')
    return template.render(
        books_rows=books_chunk,
        current_page=current_page,
        pages_count=pages_count
    )


def save_paginated_books(books, books_per_page=10, books_per_row=2):
    books_on_page = list(chunked(books, books_per_page))

    for page_num, page_books in enumerate(books_on_page, start=1):
        books_chunked = list(chunked(page_books, books_per_row))
        rendered_page = render_library_site(books_chunked,
                                            page_num,
                                            len(books_on_page))
        file_path = f'pages/index{page_num}.html'
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(rendered_page)


def main():
    load_dotenv()
    with open(os.getenv('PATH_TO_DATA_FILE', default='json_data/meta_data.json'), 'r', encoding='UTF-8') as my_file:
        books_json = json.load(my_file)
    save_paginated_books(books_json)
    server = Server()
    server.watch('template.html',
                 partial(save_paginated_books, books_json),
                 delay=1)
    server.serve(root='.')


if __name__ == '__main__':
    main()
