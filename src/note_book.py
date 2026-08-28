# Модуль для роботи з нотатками та тегами
from collections import UserDict
from typing import List, Optional
from src.models import Note 


class NoteBook(UserDict):
    """Контейнер для зберігання нотаток."""

    def add_note(self, note: Note) -> None:
        # Ключем є текст нотатки
        self.data[note.content] = note 

    def find_note(self, content: str) -> Optional[Note]:
        return self.data.get(content)

    def delete_note(self, content: str) -> bool:
        if content in self.data:
            del self.data[content]
            return True
        return False

    def search_by_text(self, query: str) -> List[Note]:
        query = query.strip().lower()
        if not query:
            return []
        
        results = []
        for note in self.data.values():
            if query in note.content.lower():
                results.append(note)
        return results

    def search_by_tag(self, tag: str) -> List[Note]:
        tag = tag.strip().lower()
        if not tag:
            return []
        
        results = []
        for note in self.data.values():
            # Приведення всіх збережених тегів до нижнього регістру
            normalized_tags = [t.strip().lower() for t in note.tags]
            if tag in normalized_tags:
                results.append(note)
        return results