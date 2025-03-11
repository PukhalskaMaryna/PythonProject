import codecs
import os


def delete_html_tags(html_file, result_file='cleaned.txt'):
    # Перевірка на існування файлу
    if not os.path.isfile(html_file):
        print(f"Файл {html_file} не знайдено!")
        return

    try:
        with codecs.open(html_file, 'r', 'utf-8') as file:
            html = file.read()

        while html.find('<') != -1:
            html = html[:html.find('<')] + html[html.find('>') + 1:]

        html = '\n'.join([html_line.lstrip() for html_line in html.splitlines() if html_line.strip() != ''])

        # Запис у результатний файл
        with codecs.open(result_file, 'w', 'utf-8') as file:
            file.write(html)
        print(f"Файл {result_file} успішно створено!")

    except Exception as e:
        print(f"Сталася помилка: {e}")


# Виклик функції
delete_html_tags('draft.html', 'cleaner.txt')
