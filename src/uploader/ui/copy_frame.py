from customtkinter import CTkFrame, CTkButton
from CTkToolTip import *


class CopyFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.copyButton = CTkButton(self, text="Copy to Clipboard", command=self.copy_button_click)
        self.copyTooltip = CTkToolTip(self.copyButton,
                                      message=f"Copies <link try> to clipboard.\n"
                                              f"Currently: 0 logs.",
                                      delay=1,
                                      justify="left")
        self.copyButton.grid(row=0, column=0, sticky="w")
        self.resetButton = CTkButton(self, text="Reset - Click Twice", command=self.reset_button_click)
        CTkToolTip(self.resetButton,
                   message="Cancel remaining uploads. Ignore running ones. Resets settings and known uploaded Logs.",
                   delay=4)
        self.resetButton.grid(row=1, column=0, sticky="w")

        self.controller = None
        self.reset = False


    def copy_button_click(self):
        if self.controller:
            self.controller.handle_copy_button()

    def reset_button_click(self):
        if not self.reset:
            self.reset = True
            self.change_reset_button_text("Reset? Click")
            return
        else:
            self.reset = False
        if self.controller:
            self.controller.handle_reset_button()

    def change_copy_button_text(self, text):
        self.copyButton.configure(text=f"{text}")

    def change_reset_button_text(self, text):
        self.copyButton.configure(text=f"{text}")

    def update_copy_tooltip_count(self, count):
        if count == 1:
            message = f"Copies 'link try' to clipboard.\nCurrently: {count} Log"
        else:
            message = f"Copies 'link try' to clipboard.\nCurrently: {count} Logs"
        self.copyTooltip.configure(message=message)
