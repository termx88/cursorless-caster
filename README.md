# Cursorless for Caster
This repository holds the [Caster](https://github.com/dictation-toolbox/Caster) side of [Cursorless](https://github.com/cursorless-dev/cursorless) (re-adapted from [cursorless-talon](https://github.com/cursorless-dev/cursorless/tree/main/cursorless-talon)).

## Installing and using
* Install [Caster](https://github.com/dictation-toolbox/Caster).
* Install [VSCode](https://code.visualstudio.com).
* Install the [VSCode Cursorless extension](https://marketplace.visualstudio.com/items?itemName=pokey.cursorless).
* Install the [VSCode Command server extension](https://marketplace.visualstudio.com/items?itemName=pokey.command-server).
* Clone to caster_user_content/rules folder.
* Restart Caster and say "enable cursor less".

### Notes:
* The Rule file is located in "src/cursorless_caster.py".
* [Official Cursorless documentation](https://www.cursorless.org/docs/).

## Project Notes
* Takes a while to cache with big kaldi. Goes up to ~5GB of RAM.
	* Due to it I set "and \<target\>" repetition max to 3 times.
	as in "\<target\> and \<target\> and \<target\> and \<target\>" being the max. 
	  If someone wants to change it, the limit is defined in the "src/compound_targets.py" file in the "get_range_repetition" function. As the "max" parameter (4 means 3 repetitions of "and \<target\>").
* "cursorless cheatsheet", might "freeze" Caster if too many settings are disabled.	
* Importing "alphabet_support" and "punctuation_support". From user directory, by importing from "caster_user_content.rules.alphabet_rules" and "caster_user_content.rules.punctuation_rules".
* Capitalization and Spacing dicts are redefined in the Rule file extras.
* Cheatsheet Legend section for [formatter] definition is 'Formatter (eg "camel", "snake"). Say "format help" for a list'. Even though "format help" is a Talon command and not in Caster. The Legend is generated extension side.
* No disabling of experimental snippets feature (currently to disable. Just comment out "from .snippets" imports, commands and extras. Defined inside cursorless_caster.py).
* Homophones not implemented.
* No changing settings folder location (currently is in "src/settings" folder).
* Doesn't Live update of lists/settings.
* No CCR and pre_phrase_signal, the latter is used for making ["Hat snapshots"](https://www.cursorless.org/docs/contributing/architecture/hat-snapshots/).
* Except for alphabet and punctuation, words are kept talon-like as in the original cursorless-talon.
