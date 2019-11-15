import tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

sync_button = Image.open('images/sync.png')
sync_image_for_button = ImageTk.PhotoImage(sync_button)
button = tk.Button(root, image=sync_image_for_button)
button.config(width="40", height="40")
button.place(x=5, y=5)
button.config(image=sync_image_for_button) 

root.mainloop()