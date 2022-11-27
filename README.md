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

## Project State
### Main problems:
* Takes a while to cache with big kaldi. Goes up to ~5GB.
	* Because of that "\<move_bring_action\> \<move_bring_targets\>" is commented out by default (in the "src/cursorless_caster.py" file).
	* Also due to it I set "and \<target\>" repetition to only 2 times.
	as in "\<target\> and \<target\> and \<target\>" being the max. 
	ex. "take brov and norway and blue prime".
	  If someone wants to change it, the limit is defined in the "src/compound_targets.py" file in the "get_range_repetition" function. As the "max" parameter (3 means 2 repetitions of "and \<target\>").

### Minor problems:
* Using kaldi values not in lexicon. Without a generator repeats multiple times. Which takes a bit of time.
* "cursorless cheatsheet", might "freeze" Caster if too many settings are disabled.	
* Importing "alphabet_support" and "punctuation_support". From user directory, by importing from "caster_user_content.rules.alphabet_rules" and "caster_user_content.rules.punctuation_rules".
* Capitalization and Spacing dicts are redefined in the Rule file extras.
* Cheatsheet Legend section for [formatter] definition is 'Formatter (eg "camel", "snake"). Say "format help" for a list'. Even though "format help" is a Talon command and not in Caster. The Legend is generated extension side.

### Not implemented:
* Disabling of experimental snippets feature (currently to disable. Just comment out "from .snippets" imports, commands and extras. Defined inside cursorless_caster.py).
* Homophones.
* Changing settings folder location (currently is in "src/settings" folder).
* Live update of lists/settings.
* CCR and pre_phrase_signal, the latter is used for making ["Hat snapshots"](https://www.cursorless.org/docs/contributing/architecture/hat-snapshots/).
* Except for alphabet and punctuation, words are kept talon-like as in the original cursorless-talon.
