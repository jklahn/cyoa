# Choose Your Own Adventure (CYOA) Engine

Ever wanted to make your own old-school choose your adventure game?  Maybe you read the R. L. Stine "Give Yourself
Goosebumps" books. Or maybe you enjoyed playing "Zork" or "The Hitchhiker's Guide to the Galaxy."  My goal was to make
it somewhat easier for folks to write their own CYOA game.  With the CYOA engine, I've tried my best to abstract as much
as possible make it easier to compose games.

# To compose games:
````
- Game data is in JSON format and read from the 'data' directory.  Use the template in the 'data' directory as a guide.
- The following attributes are required for each page:

- "name": Unique name for for page.  Pages are connected (referenced) by these names.
- "title": Titles are what are displayed when offered as choices for the player to make.
- "body": The body is the main text of the page.  It's normally the long description.
- "short_description": Shortened format of the body; when a page is re-visited, this is printed instead of the body.
- "prompt": When offered a choice(s), this the preemptive statement before the available choices.
- "linked_pages": A list of unique names (pages) that are choices for the player to make.  If pages are nodes, these are
the connected nodes.
````