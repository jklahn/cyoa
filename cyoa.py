# import the game data
from json import load
from re import findall
game_data_path = 'data/bloody_christmas.json'


class Page(object):
    def __init__(self, page, max_line_length=90):
        self.max_line_length = max_line_length
        self.name = page["name"]
        self.title = page["title"]
        self.body = self.wrap_text(page["body"])
        self.prompt = self.wrap_text(page["prompt"])
        self.short_description = page["short_description"]
        self.linked_pages = page["linked_pages"]
        self.visit_counter = 0

    def wrap_text(self, text):
        pattern = '.{1,' + str(self.max_line_length) + '}(?:\s+|$)'
        formated_text = '\n'.join(line.strip() for line in findall(pattern, text))
        return formated_text

class Book(object):
    def __init__(self, game_data):
        self.pages = {}
        self.current_page = None
        self.selection_range = 0
        self.selection = None
        self.next_page = None

        # add pages to the book
        for page in game_data["pages"]:
            self.pages[page["name"]] = Page(page)

    def read(self):
        while True:
            self.read_current_page()
            self.get_input_validate_selection()
            self.next_page = self.current_page.linked_pages[int(self.selection)]
            self.nav_to_page(self.next_page)

    def get_input_validate_selection(self):
        self.selection_range = len(self.current_page.linked_pages)
        self.selection = int(input("\nEnter a number (1 - "
                          + str(self.selection_range) + "): "))
        while int(self.selection) not in range(1, self.selection_range + 1):
            print("Invalid number")
            self.selection = int(input("\nEnter a number (1 - "
                              + str(self.selection_range) + "): "))

        self.selection -= 1

    def nav_to_page(self, page_name):
        self.current_page = self.pages[page_name]

    def read_current_page(self):
        if self.current_page.visit_counter > 0:
            print(self.current_page.short_description)
        else:
            print(self.current_page.body)

        print(self.current_page.prompt)
        self.current_page.visit_counter += 1

        for index, link in enumerate(self.current_page.linked_pages):
            print(self.pages[link].title + " [" + str(index + 1) + "]")


if __name__ == '__main__':
    with open(game_data_path) as f:
        game_data = load(f)

    book = Book(game_data)
    book.nav_to_page("start")
    book.read()


