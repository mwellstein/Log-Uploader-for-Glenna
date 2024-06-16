from datetime import datetime

from customtkinter import CTkFrame, CTkLabel, BooleanVar, CTkCheckBox


class DaySelector(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.weekLabel = CTkLabel(self, text="When did you raid?")
        self.weekLabel.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

        self.weekdaysVar = []
        self.weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        for i, day in enumerate(self.weekdays):
            day_in = BooleanVar()
            day_button = CTkCheckBox(self, text=day, variable=day_in)
            day_button.grid(row=1+i, column=0, padx=10, pady=(10, 0), sticky="w")
            self.weekdaysVar.append(day_in)

        self.controller = None

    def get_selected_days(self) -> [str]:
        # If no box is checked set to today
        if not any([day for day in self.weekdaysVar if day.get()]):
            today = datetime.now().weekday()
            self.weekdaysVar[today].set(True)
            self.update()
        return [day for i, day in enumerate(self.weekdays) if self.weekdaysVar[i].get()]
