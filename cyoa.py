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
        self.visit_counter = 0


class Book(object):
    def __init__(self, game_data):
        self.pages = {}
        self.current_page = None
        self.selection_range = 0
        self.selection = None

        # add pages to the book
        for page in game_data["pages"]:
            self.pages[page["name"]] = Page(page)

    def read(self):
        self.nav_to_page("start")
        self.read_current_page()
        self.get_input_validate_selection()
        print(self.selection)

    def get_input_validate_selection(self):
        self.selection_range = len(self.current_page.linked_pages)
        self.selection = input("\nEnter a number (1 - "
                          + str(self.selection_range) + "): ")
        while int(self.selection) not in range(1, self.selection_range):
            print("Invalid number")
            self.selection = input("\nEnter a number (1 - "
                              + str(self.selection_range) + "): ")

    def nav_to_page(self, page_name):
        self.current_page = self.pages[page_name]

    def read_current_page(self):
        print(self.current_page.body)
        print(self.current_page.prompt)

        for index, link in enumerate(self.current_page.linked_pages):
            print(self.pages[link].title + " [" + str(index + 1) + "]")


if __name__ == '__main__':
    with open(game_data_path) as f:
        game_data = load(f)

    book = Book(game_data)

    book.read()


