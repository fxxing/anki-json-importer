# anki-json-importer
JSON file importer for Anki

[Download](https://ankiweb.net/shared/info/1219378844)

# Features:

*	Import json file based on the note type fields.
*	Auto add medias.

# Usage:

1.	Create a note type named "JsonImporter", add fields and cards you need.
	example: field1, field2 
2.	The json file should be an array of objects.
	example: [{ "field1": "value1", "field2": "value2", }, ... ]
3.	On Anki menu, File > Import, then select the json file. It will import the notes to "JsonImporter" deck. It will create for you if the deck not exists.

# Media file:
If a value looks like a file path, i.e. "path/to/somefile.mp3", and the file exists, it will try to add it as media.
It supports all kinds of medias Anki supports. The file path can be an absolute path, or relative to the json file to be imported.
The extension of file name is case-insensitive.
