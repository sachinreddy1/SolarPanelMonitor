import tkinter as tk

root = tk.Tk()

newFrame = tk.Frame(root)
newFrame.grid(row=0, column=0)

# resize middle row and column
newFrame.columnconfigure(1, weight=1, minsize=100)
newFrame.rowconfigure(1, weight=1, minsize=100)

# use row/column 2 instead of 1
l1 = tk.Label(newFrame, text="a")
l1.grid(row=0,column=0)

l2 = tk.Label(newFrame, text="b")
l2.grid(row=0,column=2)

l3 = tk.Label(newFrame, text="c")
l3.grid(row=2,column=0)

l4 = tk.Label(newFrame, text="d")
l4.grid(row=2,column=2)

l = [l1, l2, l3, l4, newFrame]

def frameClick(event):
	if event.type is '4':
		color = "blue"
	if event.type is '7':
		color = "red"
	if event.type is '8':
		color = "white"

	for i in l:
		i.configure(bg=color)

for i in l:
	i.bind('<Button-1>', frameClick)
	i.bind("<Enter>", frameClick)
	i.bind("<Leave>", frameClick)

root.mainloop()