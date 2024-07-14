import json
import os
from datetime import datetime


class DiaryManager:
    def __init__(self, directory):
        self.directory = directory
        self.entries_file = os.path.join(directory, ".entries.json")
        self.entries = self.load_entries()

    def load_entries(self):
        if os.path.exists(self.entries_file):
            with open(self.entries_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save_entries(self):
        with open(self.entries_file, 'w', encoding='utf-8') as f:
            json.dump(self.entries, f, ensure_ascii=False, indent=2)

    def create_entry(self, title, content=""):
        timestamp = datetime.now().strftime("%d-%m-%Y %H:%M")
        filename = f"{timestamp.replace(' ', '_')}_{title.replace(' ', '_')}.txt"
        filepath = os.path.join(self.directory, filename)

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        entry = {
            "id": len(self.entries) + 1,
            "title": title,
            "filename": filename,
            "created_at": timestamp,
            "updated_at": timestamp
        }
        self.entries.append(entry)
        self.save_entries()
        return entry
    def read_entry(self, entry_id):
        entry = next((e for e in self.entries if e["id"] == entry_id), None)
        if entry:
            filepath = os.path.join(self.directory, entry["filename"])
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            return entry, content
        return None, None

    def update_entry(self, entry_id, title, content):
        entry = next((e for e in self.entries if e["id"] == entry_id), None)
        if entry:
            entry["title"] = title
            entry["updated_at"] = datetime.now().strftime("%d-%m-%Y %H:%M")
            filepath = os.path.join(self.directory, entry["filename"])
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            self.save_entries()
            return True
        return False

    def list_entries(self):
        return sorted(self.entries, key=lambda x: x["created_at"], reverse=True)
