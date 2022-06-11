from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle
import pyperclip
import json

FONT_NAME = "Courier"
BLACK = "#565656"
GRAY = "#DCDCDC"

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def generate_password():

    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password_input.delete(0, 'end')
    password = "".join(password_list)
    password_input.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    website = website.title()
    email = email_input.get()
    password = password_input.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if website == "" or password == "":
        messagebox.showwarning(title="Oops", message="Please don't leave any fields empty.")

    else:
        try:
            with open("data.json", mode='r') as data_file:
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", mode='w') as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", mode='w') as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_input.delete(0, 'end')
            password_input.delete(0, 'end')
            website_input.focus()


def find_password():
    website = website_input.get()
    website = website.title()
    try:
        with open("data.json", mode='r') as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Email: {data[website]['email']}"
                                                       f"\nPassword: {data[website]['password']}")
        else:
            messagebox.showinfo(title="Error", message="No details for the website exists.")


# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.config(pady=50, padx=50, bg=BLACK)
window.resizable(False, False)

canvas = Canvas(width=200, height=200, bg=BLACK, highlightthickness=0)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# Labels

website_text = Label(text="Website:", font=("Arial", 12, ""), fg=GRAY, bg=BLACK)
website_text.grid(row=1, column=0, pady=(0, 10))

email_text = Label(text="Email/Username:", font=("Arial", 12, ""), fg=GRAY, bg=BLACK)
email_text.grid(row=2, column=0, pady=(0, 10))

password_text = Label(text="Password:", font=("Arial", 12, ""), fg=GRAY, bg=BLACK)
password_text.grid(row=3, column=0, pady=(0, 10))

# Entries

website_input = Entry(width=32)
website_input.grid(row=1, column=1, sticky="EW", ipady=5, pady=(0, 10), padx=(0, 10))
website_input.focus()

email_input = Entry(width=52)
email_input.grid(row=2, column=1, columnspan=2, sticky="EW", ipady=5, pady=(0, 10))
email_input.insert(0, "joaosanson01@gmail.com")

password_input = Entry(width=32)
password_input.grid(row=3, column=1, sticky="EW", pady=(0, 10), ipady=5, padx=(0, 10))

# Buttons

generate_pass_button = Button(text="Generate Password", font="ARIAL 10", command=generate_password)
generate_pass_button.grid(column=2, row=3, sticky="WE", ipady=2, pady=(0, 10))

add_button = Button(text="Add", width=60, command=save)
add_button.grid(column=1, row=4, columnspan=2, sticky="WE", ipady=2)

search_button = Button(text="Search", font="ARIAL 10", command=find_password)
search_button.grid(column=2, row=1, columnspan=2, sticky="WE", ipady=2, pady=(0, 10))


window.mainloop()
