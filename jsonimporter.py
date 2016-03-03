#!/usr/bin/env python
# coding: utf-8
import json
import os

import anki
from anki.importing.noteimp import NoteImporter, ForeignNote
from anki.lang import _
from aqt import editor

MODEL_NAME = 'JsonImporter'
DECK_NAME = 'JsonImporter'
AUDIO_EXTENSIONS = editor.audio
IMAGE_EXTENSIONS = editor.pics
MEDIA_EXTENSIONS = editor.audio + editor.pics


class JsonImporter(NoteImporter):
    def __init__(self, col, file):
        NoteImporter.__init__(self, col, file)
        self.model = col.models.byName(MODEL_NAME)
        self.mappingFields = [f['name'] for f in self.model['flds']]
        self.mapping = None
        self.fileDir = os.path.dirname(file)

        did = col.decks.id(DECK_NAME)
        col.decks.select(did)
        deck = col.decks.get(did)
        deck['mid'] = self.model['id']
        col.decks.save(deck)

    def foreignNotes(self):
        with open(self.file, 'r') as f:
            content = f.read().decode('utf-8')

        notes = []
        entries = json.loads(content)
        for entry in entries:
            row = []
            empty = True
            for f in self.mappingFields:
                value = entry.get(f)
                if value:
                    empty = False
                    if '.' in value:
                        ext = value[value.rfind('.') + 1:].lower()
                        if ext in MEDIA_EXTENSIONS:
                            path = os.path.join(self.fileDir, value)
                            if os.path.exists(path):
                                filename = self.col.media.addFile(os.path.join(self.fileDir, value))
                                if ext in AUDIO_EXTENSIONS:
                                    value = u'[sound:%s]' % filename
                                else:
                                    value = u'<img src="%s">' % filename

                row.append(value)

            if empty:  # empty entry
                continue

            note = ForeignNote()
            note.fields = row
            notes.append(note)

        return notes

    def fields(self):
        return len(self.model['flds'])


anki.importing.Importers = anki.importing.Importers + (
    (_("Json File (*.json)"), JsonImporter),
)
