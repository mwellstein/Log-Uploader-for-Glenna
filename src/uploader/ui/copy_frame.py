from customtkinter import CTkFrame, CTkButton


class CopyFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.copyButton = CTkButton(self, text="Copy to Clipboard")
        self.copyButton.grid(row=0, column=0, sticky="w")
        self.clearCacheButton = CTkButton(self, text="Clear Uploaded")
        self.clearCacheButton.grid(row=1, column=0, sticky="w")

        self.controller = None
