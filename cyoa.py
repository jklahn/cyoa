from json import load
from os import listdir


class Page(object):
    def __init__(self, page):
        self.name = page["name"]
        self.title = page["title"]
        self.body = wrap_text(page["body"])
        self.prompt = wrap_text(page["prompt"])
        self.short_description = page["short_description"]
        self.linked_pages = page["linked_pages"]
        self.visit_counter = 0
        self.change_health = page.get("change_health")  # Get the health change for the page if it exists
        self.add_to_inventory = page.get("add_to_inventory")
        self.remove_from_inventory = page.get("remove_from_inventory")
        self.check_in_inventory = page.get("check_in_inventory")
        self.inventory_alt_page = page.get("inventory_alt_page")


class Book(object):
    def __init__(self, game_data):
        self.pages = {}
        self.current_page = None
        self.selection_range = 0
        self.selection = None
        self.next_page = None
        self.prev_page = None
        self.max_line_length = max_line_length

        # add pages to the book
        for page in game_data["pages"]:
            self.pages[page["name"]] = Page(page)

        # set state
        self.start_health = game_data["starting_health"]
        self.health = self.start_health
        self.welcome_message = wrap_text(game_data["welcome_message"])
        self.inventory = []

    def read(self):
        while True:
            self.check_inventory()
            self.read_current_page()
            if self.check_health() is False:  # Start over if dead
                break
            self.get_input_validate_selection()
            self.next_page = self.current_page.linked_pages[int(self.selection)]
            self.prev_page = self.current_page
            self.nav_to_page(self.next_page)

    def get_input_validate_selection(self):
        self.selection_range = len(self.current_page.linked_pages)
        while True:
            try:
                self.selection = 0
                while int(self.selection) not in range(1, self.selection_range + 1):
                    print("")
                    self.read_prompt()

                    if self.selection_range < 2:
                        self.selection = int(input("\nEnter a number ("
                                                   + str(self.selection_range) + "): "))
                    else:
                        self.selection = int(input("\nEnter a number (1 - "
                                                   + str(self.selection_range) + "): "))

                    if int(self.selection) not in range(1, self.selection_range + 1):
                        print("\nInvalid selection.  Try again.")

                self.selection -= 1
                break

            except ValueError:
                print("\nInvalid selection.  Try again.")
                continue

    def nav_to_page(self, page_name):
        self.current_page = self.pages[page_name]

    def read_current_page(self):
        print("")
        self.print_title()
        if self.current_page.visit_counter > 0:
            print(self.current_page.short_description)
        else:
            print(self.current_page.body)
        input("\nPress any key to continue...")

    def print_title(self, title=None):
        if title is None:
            title = self.current_page.title
        else:
            title = title
        title_length = len(title)
        top_and_bottom_bar_str = ""
        spaces_between_title_str = ""
        top_and_bottom_bar_length = int(self.max_line_length)
        amount_spaces_between_title = int((top_and_bottom_bar_length - title_length - 2) / 2)
        for i in range(0, top_and_bottom_bar_length):
            top_and_bottom_bar_str += "*"

        for i in range(0, amount_spaces_between_title):
            spaces_between_title_str += " "

        print("\n")
        print(top_and_bottom_bar_str)
        print("*" + spaces_between_title_str + title + spaces_between_title_str + "*")
        print(top_and_bottom_bar_str)

    def read_prompt(self):
        print(self.current_page.prompt)
        self.current_page.visit_counter += 1

        for index, link in enumerate(self.current_page.linked_pages):
            print(self.pages[link].title + " [" + str(index + 1) + "]")

    def check_health(self):
        if self.current_page.change_health:  # add or subtract health
            print("")
            if self.current_page.change_health > 0:
                print("+" + str(self.current_page.change_health) + " health")

            else:
                print(str(self.current_page.change_health) + " health")

            self.health += self.current_page.change_health

            if self.health > 100:  # Can't let health go over 100
                self.health = 100

            print("Current Health: " + str(self.health))

        if self.health <= 0:  # Game Over if your health goes below 0
            print("Your health has dropped below 0.")
            self.print_title('GAME OVER')
            input("Press Enter to restart...")
            return False

    def check_inventory(self):
        if self.current_page.add_to_inventory:
            if self.current_page.add_to_inventory not in self.inventory:
                self.inventory.append(self.current_page.add_to_inventory)  # add to inventory

            self.remove_page_from_all_linked_pages(self.current_page.name)  # remove page so it can't be accessed again
            print(self.current_page.body)
            self.check_health()
            print("\nCurrent Inventory:")
            print(self.inventory)
            self.nav_to_page(self.current_page.inventory_alt_page)

        if self.current_page.remove_from_inventory and self.current_page.remove_from_inventory in self.inventory:
            self.inventory.remove(self.current_page.remove_from_inventory)  # remove from inventory if present
            self.remove_page_from_all_linked_pages(self.current_page.name)  # remove page so it can't be accessed again
            print(self.current_page.body)
            print("\nCurrent Inventory:")
            print(self.inventory)
            self.nav_to_page(self.current_page.inventory_alt_page)

        if self.current_page.check_in_inventory and self.current_page.check_in_inventory in self.inventory:
            self.nav_to_page(self.current_page.inventory_alt_page)   # use alt page links if present in inventory

    def remove_page_from_all_linked_pages(self, page_name):
        for key, page in self.pages.items():
            if page_name in page.linked_pages:
                page.linked_pages.remove(page_name)


def get_data_file_path():
    for file in listdir('data/'):
        if file.endswith('.json'):
            return 'data/' + file

    print("ERROR: Failed to find a '.json' game data file in the 'data' directory.")


def wrap_text(text):
    formatted_text = ""
    for string in text.split("\n"):
        if len(string) > max_line_length:  # if the string is greater than the max allowed per line
            line = ""
            for word in string.split():  # split string into words if greater than max
                if len(line) + len(word) > max_line_length:
                    formatted_text += "\n" + line
                    line = "" + word + " "
                else:
                    line += word + " "

            formatted_text += "\n" + line
        else:
            string += "\n"  # add the new line back
            formatted_text += string

    return formatted_text


if __name__ == '__main__':

    while True:
        # open the and load the first json file in /data
        with open(get_data_file_path()) as f:
            game_data = load(f)
        max_line_length = game_data["max_line_length"]
        book = Book(game_data)
        print(book.welcome_message)
        book.nav_to_page("start")
        book.read()
