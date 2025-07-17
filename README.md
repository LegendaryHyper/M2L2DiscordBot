# M2L2DiscordBot
## Purpose and Usage
This Discord bot is intended to be a general all-in-one tool, still undergoing improvement and has been created as a part of a Python course which the developer is taking.
Pictures examplifying the usage of the bot can be seen in the "ExampleScreenshots" folder.
### !NOTICE! The bot is currently designed in Turkish. English is planned to be added afterwards.
## Added Commands
```
!go - Creates a pokemon under the username of the user, adds them to a dict (this is planned to be changed to a database instead) and returns messages stating the name, hp, xp, class and picture of the said pokemon.
!info - Returns the same output of the already created bot as the *!go* command.
!feedPokemon - Feeds the user's pokemon, letting the pokemon gain EXP and HP.
!attack @user - Attacks the @mentioned user
~~!totalPokemons - Returns total amount of pokemons created.~~ This is not yet implemented.
```
## Pokemon Classes
Default: Does not have any special trait.
Wizard: 1/5 chance of blocking an attack, shorter "!feed" cooldown.
Fighter: Higher damage (super attack.) The "!feed" command heals ~1.67x times compared to the other two classes.