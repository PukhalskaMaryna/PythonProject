def popular_words (text: str, words: list):
    """
    :param text: рядок
    :param words: список слів у нихньому регістрі
    :return: словник, у якому ключами є шукані слова та значеннями, скільки разів кожнє слово зустрічаються у орігінальному тексті
    """
    text = text.lower().split()
    dic = {}
    for word in words:
        dic[word] = text.count(word)
    return dic

assert popular_words('''When I was One I had just begun When I was Two I was nearly new ''', ['i', 'was', 'three', 'near']) == { 'i': 4, 'was': 3, 'three': 0, 'near': 0 }, 'Test1'
print('OK')