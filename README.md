# BeestLex

## IRC-legible US English dictionary definitions for Limnoria

### requires

Python 3, Limnoria, Requests, and a [Merriam-Webster Dictionary API key](https://dictionaryapi.com)

### usage

```lex <word>```

The overall goal is to balance completeness with concise IRC legibility. More
definition features may be added, but keeping it lean and mean is the order
of the day. Reducing everything to a one-liner while letting Limnoria's `more`
do most of the work (and using colours and icons to aid reading) seems to be
the ideal solution right now, but this may change in the future.

Probably full of bugs and edge-cases I haven't spotted yet, but works well
enough thus far. Thesaurus is probably upcoming.
