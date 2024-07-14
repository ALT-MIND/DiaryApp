import customtkinter as ctk


class CustomMessagebox(ctk.CTkToplevel):
    def __init__(self, master, title, message):
        super().__init__(master)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)

        self.update_idletasks()
        x = master.winfo_x() + (master.winfo_width() // 2) - (self.winfo_width() // 2)
        y = master.winfo_y() + (master.winfo_height() // 2) - (self.winfo_height() // 2)
        self.geometry(f"+{x}+{y}")

        self.label = ctk.CTkLabel(self, text=message, wraplength=250)
        self.label.pack(pady=20)

        self.button = ctk.CTkButton(self, text="OK", command=self.destroy)
        self.button.pack(pady=10)

        self.grab_set()
        self.focus_set()
        self.wait_window()
