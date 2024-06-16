from customtkinter import CTkFrame, CTkButton, BooleanVar, CTkProgressBar, CTkCheckBox


class UploadFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.uploadBtn = CTkButton(self, text="Start Upload", command=self.upload_button_click)
        self.uploadBtn.grid(row=0, column=0, sticky="w")
        # TODO: remove or use this - Use: If set ignore (not delete) known_uploaded_list (tbi)
        self.reupVar = BooleanVar()
        self.reuploadCheck = CTkCheckBox(self, text="Reupload", variable=self.reupVar)
        self.reuploadCheck.grid(row=0, column=1, sticky="w")
        # TODO: Check Progressbar
        self.uploadPrg = CTkProgressBar(self, width=400, height=20, mode="determinate")  # make indeterminate?
        self.uploadPrg.set(0)
        self.uploadPrg.grid(row=1, column=0, padx=20, pady=20, columnspan=3, sticky="w")

        self.raidVar = BooleanVar()
        self.raidVar.set(True)
        self.raidCheck = CTkCheckBox(self, text="Raids", variable=self.raidVar)
        self.raidCheck.grid(row=2, column=0, sticky="w")
        self.strikeVar = BooleanVar()
        self.strikeVar.set(True)
        self.strikeCheck = CTkCheckBox(self, text="Strikes", variable=self.strikeVar)
        self.strikeCheck.grid(row=2, column=1, sticky="w")
        self.fracVar = BooleanVar()
        self.fracCheck = CTkCheckBox(self, text="Fractals", variable=self.fracVar)
        self.fracCheck.grid(row=2, column=2, sticky="w")

        self.controller = None

    def upload_button_click(self):
        self.change_button_text("Collecting")
        self.toggle_button_state()
        self.update()

        if self.controller:
            self.controller.handle_upload_button()

    def change_button_text(self, text: str):
        self.uploadBtn.configure(text=f"{text}")

    def toggle_button_state(self):
        if self.uploadBtn.cget("state") == "disabled":
            self.uploadBtn.configure(state="enabled")
        else:
            self.uploadBtn.configure(state="disabled")

    def get_checked_categories(self) -> (bool, bool, bool):
        """Returns if (raids, strikes, fractals) should be uploaded."""
        return self.raidVar.get(), self.strikeVar.get(), self.fracVar.get()

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
