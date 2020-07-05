# beestLex

## simple, IRC-legible English dictionary definitions for Limnoria

### requires

Python 3, Limnoria, Requests, and a [Merriam-Webster Dictionary API key](https://dictionaryapi.com)

### usage

```lex <word>```

The overall goal is to balance completeness with concise IRC legibility.
Reducing everything to a one-liner while letting Limnoria's `more` do most
of the work (and using colors/attributes and icons to aid reading) seems to
be the ideal solution right now, but this may change in the future.
Additional features may be added but generally kept to a minimum in order to
maximise readability and usefulness on IRC.

This will likely remain incompetently-crafted spaghetti code and is probably
full of bugs and edge-cases I haven't spotted yet, but it works well enough
thus far.

```ety <word>``` gives word etymologies. This is probably full of boogs at
the moment.

Basic thesaurus lookups are available with an accompanying MW Thesaurus key
by using ```syn```.
