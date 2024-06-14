from customtkinter import CTkFrame, CTkLabel, CTkSegmentedButton, StringVar


class WeekSelector(CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.pastLabel = CTkLabel(self, text="Select week to upload:")
        self.pastLabel.grid(row=0, column=0, sticky="w")

        self.weeks = ["Current", "Last", "Second Last"]
        self.week_selected_element = StringVar()
        self.week = CTkSegmentedButton(self, values=self.weeks, variable=self.week_selected_element, dynamic_resizing=False, width=400)
        self.week.set(self.weeks[0])
        self.week.grid(row=1, column=0, sticky="w")
        # Can also use this.week.get to get the string instead of the StringVar

        self.controller = None

    def get_week_delta(self):
        return self.weeks.index(self.week_selected_element.get())

