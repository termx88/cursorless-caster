# Cursorless for Caster
This repository holds the Caster side of Cursorless (re-adapted from Talon).

## Installing and using
* Install [Caster](https://github.com/dictation-toolbox/Caster).
* Install [VSCode](https://code.visualstudio.com).
* Install the [VSCode Cursorless extension](https://marketplace.visualstudio.com/items?itemName=pokey.cursorless).
* Install the [VSCode Command server extension](https://marketplace.visualstudio.com/items?itemName=pokey.command-server).
* Clone to caster_user_content/rules folder.
* Restart Caster and say "enable cursor less".

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

### Not implemented:
* Homophones.
* Snippets.
* Reformat.
* Changing settings folder location (currently is in "src/settings" folder).
* Live update of lists/settings.
* CCR and pre_phrase_signal, the latter is used for making ["Hat snapshots"](https://www.cursorless.org/docs/contributing/architecture/hat-snapshots/).
* Except for alphabet and punctuation, words are kept talon-like as in the original cursorless-talon.

### Likely happens in cursorless-talon as well:
* Sometimes throws "Must use command-server extension for advanced commands"
		and requires visual studio code reboot.
		
### Other notes:
* The Rule file is located in "src/cursorless_caster.py". 
* Importing "alphabet_support" and "punctuation_support". From user directory, by importing from "caster_user_content.rules.alphabet_rules" and "caster_user_content.rules.punctuation_rules".
* Might be a bit outdated to latest official cursorless-talon.	

## Main Cursorless project
[Cursorless documentation](https://www.cursorless.org/docs/).

Cursorless is hosted as a monorepo at [`cursorless`](https://github.com/cursorless-dev/cursorless), and the source of truth for the talon files is in the [`cursorless-talon`](https://github.com/cursorless-dev/cursorless/tree/main/cursorless-talon) subdirectory.
