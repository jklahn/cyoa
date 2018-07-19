# Python-based Choose Your Own Adventure (CYOA) Engine
Ever wanted to make your own old-school choose your adventure game?  Maybe you read the R. L. Stine "Give Yourself
Goosebumps" books. Or maybe you enjoyed playing "Zork" or "The Hitchhiker's Guide to the Galaxy."  My goal was to make
a platform that made it easier for others to write their own CYOA game.  With the CYOA engine, I've tried my best to
abstract as much as possible make it easier to compose games.

## To play the game:
Games can be played using two different methods:
1) Command Line (for the nerds out there): Run 'cyoa.py' using Python 3: `python3 cyoa.py`
2) Flask Web App (preferred):
- Install flask (if it's not already installed): `pip3 install flask`
- Navigate into the flaskapp directory: `cd flaskapp`
- Run 'cyoa_app.py': `python3 cyoa_app.py`
- In a browser, navigate to port 5000: `http://localhost:5000`

## To compose games:
Game data is written in JSON format and read from the first .json file seen in the `flaskapp/data` directory.  Use the `template.json` file in
 the `flaskapp/data` directory as a reference.

**The following attributes are required for each page:**
- `"name"`: Unique name for for page.  Pages are connected (referenced) by these names.
- `"title"`: Titles are what are displayed when a page is offered as a choice for the player to make (via "linked_pages").
- `"body"`: The body is the main text of a page.  It's normally the long description.
- `"short_description"`: Shortened format of the body; when a page is re-visited, this is printed instead of the body.
- `"prompt"`: When offered a choice(s), this the preemptive statement before the available choices are printed.
- `"linked_pages"`: A list of unique names (pages) that are choices for the player to make.  If pages are though of as
nodes, these are the connected nodes.

**The following attributes are optional for pages:**
- `"change_health"`: If a page (choice) affects a players health, this attribute can increase or decrease health.
- `"add_to_inventory"`: If you want to add an item to the players inventory, use this attribute.  Use "inventory_alt_page"
to define what page to go to next after adding to inventory.
- `"remove_from_inventory"`: Removes an item from a players inventory if the item is present.  Use "inventory_alt_page"
to define what page to go to next after removing from inventory.
- `"check_in_inventory"`: Checks if a certain item is in a players inventory.  Use in conjunction with "inventory_alt_page"
- `"inventory_alt_page"`: Use in conjunction with "check_in_inventory"; if item is in inventory, use this page.
- `"visits_allowed"`: The maximum amount of times a certain page can be visited.  Once the maximum is reached, it is removed
from all linked pages.

**The following 'book' attributes are required:**
- `"starting_health"`: Defines the health amount when the game is started.
- `"welcome_message"`: Defines welcome message at the start of the game.  It's printed only once at the beginning.
- `"max_line_length"`: Sets the maximum length of each line that is printed during the game.  Otherwise, things look ugly.
- `"about_author"` (can be empty): Displayed in the 'About' page of the flask version of the game.
- `"author_website"` (can be empty): Displayed in the 'About' page of the flask version of the game.

**Tips:**
- Build out the world (make empty/placeholder pages) before adding detailed content and descriptions.  This will help you better
visualize, plan, and structure your game.
- Adding or removing something from inventory requires a separate 'page'/node be created.  Once the inventory page has
been visited in-game, it will be removed from all linked pages.  This prevents the page from being re-visited.
- Because text is stored in JSON format, make sure to escape characters where needed:
````
- Double quote is replaced with \"
- Newline is replaced with \n
- Backspace is replaced with \b
- Form feed is replaced with \f
- Carriage return is replaced with \r
- Tab is replaced with \t
- Backslash is replaced with \\
````
