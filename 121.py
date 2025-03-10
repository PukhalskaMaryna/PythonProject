import codecs
def delete_html_tags(html_file, result_file='cleaned.txt'):
      with codecs.open(html_file, 'r', 'utf-8') as file:
           html = file.read()

      while html.find('<') != -1:
        html = html[ : html.find('<')] + html[html.find('>') + 1 : ]

      html = '\n'.join([html_line for html_line in html.splitlines() if html_line.strip() != ''])

      with codecs.open(result_file, 'w', 'utf-8') as file:
          file.write(html)

delete_html_tags('draft.html')