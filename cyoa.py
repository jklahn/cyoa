# import the game data
from json import load
game_data_path = 'data/bloody_christmas.json'


class Page(object):
    def __init__(self, page):
        self.name = page["name"]
        self.title = page["title"]
        self.body = page["body"]
        self.prompt = page["prompt"]
        self.linked_pages = page["linked_pages"]


if __name__ == '__main__':
    with open(game_data_path) as f:
        data = load(f)

    book = {}
    for page in data["pages"]:
        book[page["name"]] = Page(page)

    current_page = book["start"]

    print(current_page.body)
    print(current_page.prompt)

    for index, link in enumerate(current_page.linked_pages):
        print(link + " [" + str(index + 1) + "]")
