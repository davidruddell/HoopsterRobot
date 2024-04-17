import customtkinter

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

root = customtkinter.CTk()
root.geometry("800x480")
root.title('Hoopster - Basketball Shooting Robot')

def login():
    print("Test")

def launch_button():
        print("launched")

def set_button():
     print("set")

def abort_button():
    print("aborted")

frame = customtkinter.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)

label = customtkinter.CTkLabel(master=frame, text="HOOPSTER", font=('Arial Black', 50))
label.pack(pady=12, padx=10)

entry1 = customtkinter.CTkEntry(master=frame, placeholder_text="text1")
entry1.pack(pady=12, padx=10)

entry2 = customtkinter.CTkEntry(master=frame, placeholder_text="text2")
entry2.pack(pady=12, padx=10)

launchButton = customtkinter.CTkButton(master=frame, text="Launch Button", command=launch_button)
launchButton.pack(pady=12, padx=10)

setButton = button = customtkinter.CTkButton(master=frame, text="Set Button", command=set_button)
setButton.pack(pady=12, padx=10)

abortButton = customtkinter.CTkButton(master=frame, text="Abort Button", command=abort_button)
abortButton.pack(pady=12, padx=10)



checkbox = customtkinter.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)

root.mainloop()
