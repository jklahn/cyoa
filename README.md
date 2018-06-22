# Python-based Choose Your Own Adventure (CYOA) Engine

Ever wanted to make your own old-school choose your adventure game?  Maybe you read the R. L. Stine "Give Yourself
Goosebumps" books. Or maybe you enjoyed playing "Zork" or "The Hitchhiker's Guide to the Galaxy."  My goal was to make
a platform that made it easier for others to write their own CYOA game.  With the CYOA engine, I've tried my best to
abstract as much as possible make it easier to compose games.

# To compose games:
Game data is written in JSON format and read from the .json file in the `data` directory.  Use the `template.json` file in
 the `data` directory as a guide.

The following attributes are required for each page:

- `"name"`: Unique name for for page.  Pages are connected (referenced) by these names.
- `"title"`: Titles are what are displayed when a page is offered as a choice for the player to make (via "linked_pages").
- `"body"`: The body is the main text of a page.  It's normally the long description.
- `"short_description"`: Shortened format of the body; when a page is re-visited, this is printed instead of the body.
- `"prompt"`: When offered a choice(s), this the preemptive statement before the available choices are printed.
- `"linked_pages"`: A list of unique names (pages) that are choices for the player to make.  If pages are though of as
nodes, these are the connected nodes.

The following attributes are optional for pages:
- `"change_health"`: If a page (choice) affects a players health, this attribute can increase or decrease health.
- `"add_to_inventory"`: If you want to add an item to the players inventory, use this attribute.
- `"remove_from_inventory"`: Removes an item from a players inventory if the item is present.
- `"check_in_inventory"`: Checks if a certain item is in a players inventory.
- `"inventory_alt_page"`: Use in conjunction with "check_in_inventory"; if item is in inventory, use this page.

Misc:
- `"starting_health"` (required): Defines the health amount when the game is started.

