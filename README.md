Choose Your Own Adventure (CYOA) Engine

Ever wanted to make your own old-school choose your adventure game?  Maybe you read the R. L. Stine "Give Yourself
Goosebumps" books. Or maybe you enjoyed playing "Zork" or "The Hitchhiker's Guide to the Galaxy."  My goal was to make
it somewhat easier for folks to write their own CYOA game.  With the CYOA engine, I've tried my best to abstract as much
as possible make it easier to compose games.

To compose games:

- Game data is in JSON format and read from the 'data' directory.  Use the template in the 'data' directory as a guide.
- The following 'page' attributes are mandatory:
"name", "title", "body", "short_description", "prompt", "linked_pages"