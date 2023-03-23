#[Reminder_bot](https://t.me/nllllibeth_reminder_bot)
***
## Description

Written in Python using [Aiogram](https://aiogram.dev/), a tool that reminds a user with their own messages at specified time, using [Apscheduler](https://apscheduler.readthedocs.io/en/3.x/). 

Written in Python using [Aiogram](https://aiogram.dev/), a tool with that a user can set a reminder with their own messages, frequency, time and the bot will send notifications with setted message according to specified time, using [Apscheduler](https://apscheduler.readthedocs.io/en/3.x/). 

***

## GIF demo

<img src="https://gifyu.com/image/SIkX4/">


***

## Installation Guide

#### Local Setup
> The setup given here is for a linux environment (Debian/Ubuntu)

- Clone to the local machine 

        $ git clone https://github.com/
        $ cd currency_bot

- Create and activate virtual environment 

        $ python3 -m venv venv
        $ source venv/bin/activate

- Install dependencies 

        $ pip3 install -U -r requirements.txt


#### Environment Variables

For proper running the bot you need toset your own environment variable:

- `TOKEN_REMINDER` - Get your bot token from [Bot Father](https://t.me/BotFather)

#### Run bot
        $ python bot_file.py 
After this command go to bot in [Telegram](https://t.me/nllllibeth_reminder_bot) with the link from [Bot Father](https://t.me/BotFather), and run `/start` command. You will see welcome message. 

*** 

## Supported commands and functions 

#### Commands
- `/start` - Command to start bot or check whether the bot is working or not
- `/help` - Command with the same purpose as `/start`
- `/set` - Command to set a new reminder 
- `/edit` - Command to edit the existing reminder from the list of your reminders
- `/stop` - Command to stop and delete the existing reminder from the list of your reminders

#### Functions

After completing the form with reminder's name, message, frequency, and time user's reminder will be set and the bot will send them a message at user's specified time. More details:

- `Choose a command`, `Choose frequency` - Inline keyboards're used to intetact with a user, and response them
- `Send location` - Automatical identification a user's timezone using their  location with the help of [Nominatim](https://nominatim.org/) 
- `Choose a reminder to edit/stop` - Show inline buttons with the list of setted reminders for particular user, for further execution `/edit`, `/stop` commands
- `Send message` - After filling the form with user's data new jobs to scheduler for sending messages will be created.

***

## Contact 

You can contact me [@nllllibeth](https://t.me/nllllibeth)