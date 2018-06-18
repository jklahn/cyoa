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
        formatted_text = ""
        for string in text.split("\n"):
            if len(string) > self.max_line_length:  # if the string is greater than the max allowed per line
                line = ""
                for word in string.split():  # split string into words if greater than max
                    if len(line) > self.max_line_length:
                        formatted_text += "\n" + line
                        line = "" + word + " "
                    else:
                        line += word + " "

                formatted_text += "\n" + line
            else:
                string += "\n"  # add the new line back
                formatted_text += string

        return formatted_text


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


