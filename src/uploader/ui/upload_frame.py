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
        if self.controller:
            self.controller.handle_upload_button()

    def get_checked_categories(self):
        return self.raidVar.get(), self.strikeVar.get(), self.fracVar.get()

    def update_progess(self, val):
        if val > 1:
            val = 1
        if val < 0:
            val = 0
        self.uploadPrg.set(val)
        self.update_idletasks()
