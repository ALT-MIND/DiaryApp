import customtkinter as ctk
from diary_manager import DiaryManager
from custom_widgets import CustomMessagebox
import filedialpy
import os


class DiaryGUI:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Щоденник")
        self.root.geometry("600x450")

        self.diary_manager = None
        self.choose_directory()

        if self.diary_manager:
            self.create_widgets()
            self.show_entries_list()
        else:
            self.root.quit()

    def choose_directory(self):
        directory = filedialpy.openDir()

        if directory:
            if self.is_valid_directory(directory):
                self.diary_manager = DiaryManager(directory)
            else:
                CustomMessagebox(self.root, "Помилка",
                                 "Вибрана папка не є порожньою і не містить базу даних щоденника.")
                self.root.quit()
        else:
            # Якщо папку не вибрано, завершуємо роботу програми
            self.root.quit()

    def is_valid_directory(self, directory):
        contents = os.listdir(directory)
        return len(contents) == 0 or ".entries.json" in contents

    def create_widgets(self):
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(pady=5, padx=5, fill="both", expand=True)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_entries_list(self):
        self.clear_content_frame()
        self.current_page = "list"

        entries_frame = ctk.CTkScrollableFrame(self.content_frame)
        entries_frame.pack(fill="both", expand=True, pady=(0, 5))

        entries = self.diary_manager.list_entries()
        for entry in entries:
            entry_frame = ctk.CTkFrame(entries_frame)
            entry_frame.pack(pady=2, padx=5, fill="x")

            ctk.CTkLabel(entry_frame, text=f"{entry['title']} ({entry['created_at']})").pack(side="left", padx=5)
            ctk.CTkButton(entry_frame, text="Перегляд", command=lambda e=entry: self.show_view_page(e)).pack(
                side="right", padx=2)
            ctk.CTkButton(entry_frame, text="Редагувати", command=lambda e=entry: self.show_edit_page(e)).pack(
                side="right", padx=2)

        new_entry_button = ctk.CTkButton(self.content_frame, text="Новий запис", command=self.show_new_entry_page)
        new_entry_button.pack(pady=5)

    def show_view_page(self, entry):
        self.clear_content_frame()
        self.current_page = "view"

        entry_data, content = self.diary_manager.read_entry(entry['id'])

        ctk.CTkLabel(self.content_frame, text=entry_data['title'], font=("Arial", 16, "bold")).pack(pady=5)
        ctk.CTkLabel(self.content_frame, text=f"Створено: {entry_data['created_at']}").pack()
        ctk.CTkLabel(self.content_frame, text=f"Оновлено: {entry_data['updated_at']}").pack()

        content_text = ctk.CTkTextbox(self.content_frame, width=580, height=300)
        content_text.pack(pady=5)
        content_text.insert("1.0", content)
        content_text.configure(state="disabled")

        ctk.CTkButton(self.content_frame, text="Назад до списку", command=self.show_entries_list).pack(pady=5)

    def show_edit_page(self, entry):
        self.clear_content_frame()
        self.current_page = "edit"

        entry_data, content = self.diary_manager.read_entry(entry['id'])

        title_var = ctk.StringVar(value=entry_data['title'])

        ctk.CTkLabel(self.content_frame, text="Редагування запису").pack(pady=5)
        ctk.CTkEntry(self.content_frame, textvariable=title_var, width=580).pack(pady=5)
        content_text = ctk.CTkTextbox(self.content_frame, width=580, height=300)
        content_text.pack(pady=5)
        content_text.insert("1.0", content)

        def save_changes():
            new_title = title_var.get()
            new_content = content_text.get("1.0", ctk.END).strip()
            self.diary_manager.update_entry(entry_data['id'], new_title, new_content)
            self.show_entries_list()

        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=5)
        ctk.CTkButton(button_frame, text="Зберегти зміни", command=save_changes).pack(side="left", padx=2)
        ctk.CTkButton(button_frame, text="Скасувати", command=self.show_entries_list).pack(side="left", padx=2)

    def show_new_entry_page(self):
        self.clear_content_frame()
        self.current_page = "new"

        ctk.CTkLabel(self.content_frame, text="Новий запис").pack(pady=5)
        title_entry = ctk.CTkEntry(self.content_frame, width=580, placeholder_text="Назва запису")
        title_entry.pack(pady=5)
        content_text = ctk.CTkTextbox(self.content_frame, width=580, height=300)
        content_text.pack(pady=5)

        def save_new_entry():
            title = title_entry.get()
            content = content_text.get("1.0", ctk.END).strip()
            if title:
                self.diary_manager.create_entry(title, content)
                self.show_entries_list()
                CustomMessagebox(self.root, "Успіх", "Запис успішно створено")
            else:
                CustomMessagebox(self.root, "Помилка", "Будь ласка, введіть назву запису")

        button_frame = ctk.CTkFrame(self.content_frame)
        button_frame.pack(pady=5)
        ctk.CTkButton(button_frame, text="Зберегти", command=save_new_entry).pack(side="left", padx=2)
        ctk.CTkButton(button_frame, text="Скасувати", command=self.show_entries_list).pack(side="left", padx=2)

    def run(self):
        if self.diary_manager:
            self.root.mainloop()


if __name__ == "__main__":
    app = DiaryGUI()
    app.run()
