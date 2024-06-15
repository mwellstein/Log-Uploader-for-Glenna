from customtkinter import CTkFrame, CTkButton, BooleanVar, CTkProgressBar, CTkCheckBox


class UploadFrame(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.uploadBtn = CTkButton(self, text="Start Upload", command=self.upload_button_click)
        self.uploadBtn.grid(row=0, column=0, sticky="w")

        self.reupVar = BooleanVar()
        self.reuploadCheck = CTkCheckBox(self, text="Reupload", variable=self.reupVar)
        self.reuploadCheck.grid(row=0, column=1, sticky="w")

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
        self.after(2000, self.update_progress)

        if self.controller:
            self.controller.handle_upload_button()

    def get_checked_categories(self) -> (bool, bool, bool):
        """Returns if (raids, strikes, fractals) should be uploaded."""
        return self.raidVar.get(), self.strikeVar.get(), self.fracVar.get()

    def update_progress(self):
        uploaded_count = self.controller.model.uploaded_count
        if uploaded_count > 1:
            uploaded_count = 1
        if uploaded_count < 0:
            uploaded_count = 0
        self.uploadPrg.set(uploaded_count)
        self.update_idletasks()

        if not uploaded_count >= self.controller.model.collected_count:
            self.after(500, self.update_progress)
