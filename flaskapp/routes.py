from flask import Flask, render_template, request
from os import path, listdir
from json import load

app = Flask(__name__)  # create flask object


def get_game_data_file_path():
    file_path = path.join(path.abspath(path.curdir), '../data')
    for file_name in listdir(file_path):
        if file_name.endswith('.json'):
            return file_path + '/' + file_name

    print("ERROR: Failed to find a '.json' game data file in the 'data' directory.")


with open(get_game_data_file_path()) as f:  # load the game data
    game_data = load(f)


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
        health_message = ""
        if self.current_page.change_health:  # add or subtract health
            health_message += "<br/><br/>"
            if self.current_page.change_health > 0:
                health_message += ("+" + str(self.current_page.change_health) + " health<br/>")

            else:
                health_message += (str(self.current_page.change_health) + " health<br/><br/>")

            self.health += self.current_page.change_health

            if self.health > 100:  # Can't let health go over 100
                self.health = 100

            # health_message += ("<br/>Current Health: " + str(self.health))

        if self.health <= 0:  # Game Over if your health goes below 0
            health_message = "<br/>Your health has dropped below 0.<br/>"

        return health_message

    def check_inventory(self):
        if self.current_page.add_to_inventory:
            if self.current_page.add_to_inventory not in self.inventory:
                self.inventory.append(self.current_page.add_to_inventory)  # add to inventory

            self.remove_page_from_all_linked_pages(self.current_page.name)  # remove page so it can't be accessed again
            return True

        if self.current_page.remove_from_inventory and self.current_page.remove_from_inventory in self.inventory:
            self.inventory.remove(self.current_page.remove_from_inventory)  # remove from inventory if present
            self.remove_page_from_all_linked_pages(self.current_page.name)  # remove page so it can't be accessed again
            return True

        return False  # if inventory is not affected

    def remove_page_from_all_linked_pages(self, page_name):
        for key, page in self.pages.items():
            if page_name in page.linked_pages:
                page.linked_pages.remove(page_name)


def wrap_text(text, max_line_length=120):
    formatted_text = ""
    for string in text.split("\n"):
        if len(string) > max_line_length:  # if the string is greater than the max allowed per line
            line = ""
            for word in string.split():  # split string into words if greater than max
                if len(line) + len(word) > max_line_length:
                    formatted_text += "<br/>" + line
                    line = "" + word + " "
                else:
                    line += word + " "

            formatted_text += "<br/>" + line
        else:
            string += "<br/>"  # add the new line back
            formatted_text += string

    return formatted_text


def restart():
    with open(get_game_data_file_path()) as f:  # load the game data
        global game_data
        game_data = load(f)

    global max_line_length
    max_line_length = game_data["max_line_length"]

    global book
    book = Book(game_data)
    book.nav_to_page("start")
    book.health = book.start_health
    book.inventory = []


def get_current_linked_pages():
    linked_pages = {}
    for page_link in book.current_page.linked_pages:
        linked_pages[page_link] = book.pages[page_link].title

    return linked_pages


def get_page_body():
    if book.current_page.visit_counter > 0:
        return book.current_page.short_description
    else:
        return book.current_page.body


def build_page_contents():
    # get the page body
    page_body = get_page_body()

    # Check if adding to inventory
    if book.current_page.add_to_inventory:
        book.inventory.append(book.current_page.add_to_inventory)  # add to inventory
        book.remove_page_from_all_linked_pages(book.current_page.name)  # remove page so it can't be accessed again
        book.nav_to_page(book.current_page.inventory_alt_page)

        page_body += '<br/>Current Inventory:<br/>' + str(book.inventory)  # add current inventory to the page

        health_message = book.check_health()  # check for a change in health

        if health_message:  # add health message to the page if there is one

            page_body += health_message

            if 'Your health has dropped below 0' in health_message:
                prompt = "<br/>GAME OVER<br/>"
                linked_pages = {}
                return page_body, prompt, linked_pages
        prompt = ""
        linked_pages = {book.current_page.name: 'Continue'}

    # Check if removing from inventory
    elif book.current_page.remove_from_inventory and book.current_page.remove_from_inventory in book.inventory:
        book.inventory.remove(book.current_page.remove_from_inventory)  # remove from inventory if present
        book.remove_page_from_all_linked_pages(book.current_page.name)  # remove page so it can't be accessed again
        book.nav_to_page(book.current_page.inventory_alt_page)

        if book.inventory:
            page_body += '<br/>Current Inventory:<br/>' + str(book.inventory)
        else:
            page_body += '<br/><br/>Current Inventory:<br/>[Empty]<br/>'

        health_message = book.check_health()  # check for a change in health

        if health_message:  # add health message to the page if there is one

            page_body += health_message

            if 'Your health has dropped below 0' in health_message:
                prompt = "<br/>GAME OVER<br/>"
                linked_pages = {}
                return page_body, prompt, linked_pages

        prompt = ""
        linked_pages = {book.current_page.name: 'Continue'}

    # Page is checking if something is in inventory to decide next pages
    elif book.current_page.check_in_inventory and book.current_page.check_in_inventory in book.inventory:
        book.nav_to_page(book.current_page.inventory_alt_page)
        page_body = get_page_body()

        health_message = book.check_health()  # check for a change in health

        if health_message:  # add health message to the page if there is one

            page_body += health_message

            if 'Your health has dropped below 0' in health_message:
                prompt = "<br/>GAME OVER<br/>"
                linked_pages = {}
                return page_body, prompt, linked_pages

        linked_pages = get_current_linked_pages()
        prompt = book.current_page.prompt

    # Do a final health check if it wasn't done in an inventory check
    else:
        health_message = book.check_health()  # check for a change in health

        if health_message:  # add health message to the page if there is one

            page_body += health_message

            if 'Your health has dropped below 0' in health_message:
                prompt = "<br/>GAME OVER<br/>"
                linked_pages = {}
                return page_body, prompt, linked_pages

        linked_pages = get_current_linked_pages()
        prompt = book.current_page.prompt

    return page_body, prompt, linked_pages


if __name__ == '__main__':
    @app.route('/')
    def home():
        return render_template('home.html', title=game_data["title"], welcome_message=game_data["welcome_message"])

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/start')
    def start():
        restart()

        return render_template('start.html', title=book.current_page.title, page_body=book.current_page.body,
                               prompt=book.current_page.prompt, linked_pages=get_current_linked_pages(),
                               current_health=book.health)

    @app.route('/start', methods=['POST'])
    def start_post():
        next_page = request.form.get('next-page')
        book.nav_to_page(next_page)

        page_body, prompt, linked_pages = build_page_contents()

        book.current_page.visit_counter += 1  # increment the page visit counter

        return render_template('start.html', title=book.current_page.title, page_body=page_body,
                               prompt=prompt, linked_pages=linked_pages,
                               current_health=book.health)

    app.run(debug=True, use_reloader=True)  # start flask (render web pages)
