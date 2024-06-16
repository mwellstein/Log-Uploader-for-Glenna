from customtkinter import CTkFrame, CTkButton
from CTkToolTip import CTkToolTip


class CopyFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create an inner frame
        inner_frame = CTkFrame(self, fg_color=("gray86", "gray17"))
        inner_frame.pack(anchor="center", pady=10)  # Center the inner frame

        self.copy_text = "Copy to Clipboard"
        self.copyButton = CTkButton(inner_frame, text=self.copy_text, command=self.copy_button_click)
        self.copyTooltip = CTkToolTip(self.copyButton,
                                      message=f"Copies <link try> to clipboard.\n"
                                              f"Currently 0 Logs to copy.",
                                      justify="left")
        self.copyButton.grid(row=0, column=0, pady=(5, 0), sticky="w")

        self.reset_text = "Reset - Click Twice"
        self.resetButton = CTkButton(inner_frame, text=self.reset_text, command=self.reset_button_click)
        CTkToolTip(self.resetButton,
                   message="Cancel remaining uploads. Ignore running ones.\nForget already uploaded logs/links.",
                   justify="left")
        self.resetButton.grid(row=1, column=0, pady=(30, 5), sticky="w")

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
            self.toggle_reset_button_state()
            self.update()
            self.reset = False
        if self.controller:
            self.controller.handle_reset_button()

    def toggle_reset_button_state(self):
        if self.resetButton.cget("state") == "normal":
            self.resetButton.configure(state="disabled")
        else:
            self.resetButton.configure(state="normal")

    def change_copy_button_text(self, text):
        self.copyButton.configure(text=f"{text}")

    def change_reset_button_text(self, text):
        self.resetButton.configure(text=f"{text}")

    def update_copy_tooltip_count(self, count):
        if count == 1:
            message = f"Copies 'link try' to clipboard.\nCurrently: {count} Log"
        else:
            message = f"Copies 'link try' to clipboard.\nCurrently: {count} Logs"
        self.copyTooltip.configure(message=message)

    def reset_texts(self):
        self.copyButton.configure(text=self.copy_text)

    def reset_reset_button(self):
        self.resetButton.configure(text=self.reset_text)
        self.toggle_reset_button_state()
        self.update()
