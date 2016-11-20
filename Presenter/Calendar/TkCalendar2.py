# as simple monthly calendar with Tkinter
# give calendar and Tkinter abbreviated namespaces
import calendar as cd
import Tkinter as tk
# supply year and month
year = 2015
month = 2    # jan=1
# assign the month's calendar to a multiline string
str1 = cd.month(year, month)
# create the window form and call it root (typical)
root = tk.Tk()
root.title("Monthly Calendar")
# pick a fixed font like courier so spaces behave right
label1 = tk.Label(root, text=str1, font=('courier', 14, 'bold'), bg='yellow')
label1.pack(padx=3, pady=5)
# run the event loop (needed)
root.mainloop()