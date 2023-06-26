import PySimpleGUI as sg
import json

USERS_FILE = 'users.json'
users = {}

def load_users():
    try:
        with open(USERS_FILE, 'r') as file:
            data = json.load(file)
            users.update(data)
    except FileNotFoundError:
        pass

def save_users():
    with open(USERS_FILE, 'w') as file:
        json.dump(users, file)

def signup(username, password):
    if username in users:
        sg.popup('Error', 'Username already exists. Please choose a different username.')
    else:
        users[username] = password
        sg.popup('Success', 'Account created successfully.')
        save_users()

def login(username, password):
    if username in users and users[username] == password:
        sg.popup('Success', f'Welcome, {username}! You have successfully logged in.')
        password_manager()
    else:
        sg.popup('Error', 'Invalid username or password.')

def password_manager():
    passwords = {}

    def save_password(website, username, password):
        passwords[website] = {'username': username, 'password': password}
        sg.popup('Success', f'Password for {website} saved.')
        save_passwords()

    def save_passwords():
        with open('passwords.json', 'w') as file:
            json.dump(passwords, file)

    def load_passwords():
        try:
            with open('passwords.json', 'r') as file:
                data = json.load(file)
                passwords.update(data)
        except FileNotFoundError:
            pass

    def get_saved_passwords():
        password_list = []
        for website, details in passwords.items():
            password_list.append([website, details['username'], details['password']])
        return password_list

    load_passwords()

    layout = [
        [sg.Text('Password Manager')],
        [sg.Table(get_saved_passwords(), headings=['Website', 'Username', 'Password'],
                  auto_size_columns=True, display_row_numbers=True, key='password_table')],
        [sg.Text('Website:'), sg.Input(key='website')],
        [sg.Text('Username:'), sg.Input(key='pm_username')],
        [sg.Text('Password:'), sg.Input(key='pm_password', password_char='*')],
        [sg.Button('Save'), sg.Button('Exit')]
    ]

    window = sg.Window('Password Manager', layout)

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        elif event == 'Save':
            website = values['website']
            username = values['pm_username']
            password = values['pm_password']
            save_password(website, username, password)
            window['password_table'].update(get_saved_passwords())

    window.close()

# Load existing users from file
load_users()

layout = [
    [sg.Text('Username:'), sg.Input(key='username')],
    [sg.Text('Password:'), sg.Input(key='password', password_char='*')],
    [sg.Button('Login'), sg.Button('Signup'), sg.Button('Exit')]
]

window = sg.Window('Authentication App', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Login':
        username = values['username']
        password = values['password']
        login(username, password)
    elif event == 'Signup':
        username = values['username']
        password = values['password']
        signup(username, password)

window.close()

# Save updated users to file
save_users()
