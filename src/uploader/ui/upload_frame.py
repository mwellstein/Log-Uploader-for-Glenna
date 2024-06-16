from customtkinter import CTkFrame, CTkButton, BooleanVar, CTkProgressBar, CTkCheckBox
from CTkToolTip import CTkToolTip


class UploadFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        # Create an inner frame
        inner_frame = CTkFrame(self, fg_color=("gray86", "gray17"))
        inner_frame.pack(anchor="center")  # Center the inner frame

        # Get the colors used, they alternate someway between fg and bg I assume
        # print(self.cget("fg_color"))
        # print(self.cget("bg_color"))

        self.upload_text = "Start Upload"
        self.uploadBtn = CTkButton(inner_frame, text=self.upload_text, command=self.upload_button_click)
        self.uploadBtn.grid(row=0, column=1, pady=(20, 0), sticky="w")
        self.upload_tooltip = CTkToolTip(self.uploadBtn,
                                         message="Start upload.\n"
                                                 "Will try to upload missing Logs, if any.\n"
                                                 "Auto-selects today, if nothing is selected.",
                                         justify="left")
        # TODO: Check Progressbar
        self.uploadPrg = CTkProgressBar(inner_frame, width=400, height=20, mode="determinate")  # make indeterminate?
        self.uploadPrg.set(0)
        self.uploadPrg.grid(row=1, column=0, pady=15, columnspan=3, sticky="n")

        self.raidVar = BooleanVar()
        self.raidVar.set(True)
        self.raidCheck = CTkCheckBox(inner_frame, text="Raids", variable=self.raidVar)
        self.raidCheck.grid(row=2, column=0, pady=(0, 10), sticky="n")
        self.strikeVar = BooleanVar()
        self.strikeVar.set(True)
        self.strikeCheck = CTkCheckBox(inner_frame, text="Strikes", variable=self.strikeVar)
        self.strikeCheck.grid(row=2, column=1, pady=(0, 10), sticky="n")
        self.fracVar = BooleanVar()
        self.fracCheck = CTkCheckBox(inner_frame, text="Fractals", variable=self.fracVar)
        self.fracCheck.grid(row=2, column=2, pady=(0, 10), sticky="n")

        self.controller = None

    def upload_button_click(self):
        self.change_upload_text("Collecting")
        self.toggle_button_state()
        self.update()

        if self.controller:
            self.controller.handle_upload_button()

    def change_upload_text(self, text: str):
        self.uploadBtn.configure(text=f"{text}")

    def toggle_button_state(self, disable: bool = False):
        if disable or self.uploadBtn.cget("state") == "normal":
            self.uploadBtn.configure(state="disabled")
        else:
            self.uploadBtn.configure(state="normal")

    def get_checked_categories(self) -> (bool, bool, bool):
        """Returns if (raids, strikes, fractals) should be uploaded."""
        return self.raidVar.get(), self.strikeVar.get(), self.fracVar.get()

    def update_upload_tooltip(self, message):
        self.upload_tooltip.configure(message=message)

    def update_progress(self, up_count):
        collected_count = self.controller.model.collected_count  # Is static once calculated, is fine to just grab
        if not collected_count or collected_count == 0:
            return

        up_percent = up_count / collected_count
        if up_percent > 1:
            up_percent = 1
        if up_percent < 0:
            up_percent = 0

        self.uploadPrg.set(up_percent)
        self.update_idletasks()

    def reset_texts(self):
        self.change_upload_text(self.upload_text)
