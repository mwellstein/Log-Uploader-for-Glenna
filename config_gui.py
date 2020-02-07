from tkinter import Tk, Frame, Label, Checkbutton, BooleanVar, filedialog, Button, StringVar, Entry, Spinbox, IntVar
from tkinter.ttk import Progressbar

root = Tk()
root.title("dps.report Upload Utility")
root.geometry("500x300")

left_frame = Frame(root)
left_frame.grid(column=0, row=0, sticky="N", padx=20, pady=20)

raid_days_label = Label(left_frame, text="When did you raid?")
raid_days_label.grid(row=0)


def check_days(button):
    if not button["var"].get():
        weekdays.remove(day_button["text"])
    else:
        weekdays.append(day_button["text"])
    print(button["var"].get())


weekdays = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
week_buttons = []
for i, day in enumerate(weekdays):
    print(i, day)
    day_in = BooleanVar()
    day_button = Checkbutton(left_frame, text=day, var=day_in)
    week_buttons.append(day_button)
    day_button.grid(row=i + 1, sticky="W")

right_frame = Frame(root)
right_frame.grid(column=1, row=0, sticky="NW", padx=20, pady=20)

log_path_frame = Frame(right_frame)
log_path_frame.grid(column=0, row=0, sticky="W")


def browse_button():
    global log_path, weeks_back
    dirname = filedialog.askdirectory()
    log_path.set(dirname)


log_path = StringVar()
log_path_label = Label(log_path_frame, text="Select the main log folder").grid(column=0, row=0, sticky="W")
log_path_text = Entry(log_path_frame, text=log_path, width=30).grid(column=0, row=1, sticky="W")
choose_path_button = Button(log_path_frame, text="Change", command=browse_button).grid(column=1, row=1, sticky="W")

past_weeks_frame = Frame(right_frame)
past_weeks_frame.grid(column=0, row=1, sticky="W")

past_weeks_label = Label(past_weeks_frame, text="Go back to past weeks").grid(row=0, sticky="W")
weeks_back = IntVar()
past_weeks_spin = Spinbox(past_weeks_frame, textvariable=weeks_back, from_=0, to=3, width=5).grid(row=1, sticky="W")

start_frame = Frame(right_frame)
start_frame.grid(column=0, row=2, sticky="W", pady=30)


def start():
    global progress
    progress["value"] = 50


start_button = Button(start_frame, text="Start upload", command=start).grid(column=0, row=0, sticky="W")
progress = Progressbar(start_frame, length=200, mode="determinate")
progress.grid(column=0, row=1, sticky="W", pady=10)
progress["value"] = 0
progress["maximum"] = 100

root.mainloop()
