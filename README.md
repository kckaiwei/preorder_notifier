# Preorder notification library

##Description

After much scrambling to get my hands on Nintendo Switch and Breath of the Wild Special Edition preorders,
I decided to compile all my scripts and bots used to help net me preorders into a library for others to use.

##Usage

`config.py` is being used to hold login credentials. Since these are hosted as plain text, you HAVE to be very careful
with where you host this bot. Additionally, I suggest creating an email just for this purpose, as well as a reddit
account for just this.

If you are using Gmail, it is required that you create an app password for this bot. Here is the relavent article:

https://support.google.com/accounts/answer/185833?hl=en

| Property        | Usage                      | Example text           | Type |
| --------------- |:--------------------------:| ----------------------:|-----:|
| REDDIT_USERNAME | username for reddit        | 'username'             | str  |
| REDDIT_PASSWORD | password for reddit        | 'password'             | str  |
| EMAIL_USERNAME  | email of notifier bot      | 'example@gmail.com'    | str  |
| EMAIL_PASSWORD  | password of notifier email | 'password'             | str  |
| TO_ADDRESS      | email to be notified       | '9999999999@vtext.com' | str  |

You can send messsages to a cell phone through text is you use a SMS gateway for your corresponding carrier.

##Putting the bot on Heroku

First you need to create a Heroku Account. This can be done for free since we're only interested in using a small fraction of the dyno time. Dynos are containers that can be thought of as a bare minimum computer (not really a computer, but think of it like one) that installs only what you need and runs your programs. Heroku lets you use one dyno for 16 hours of uptime. Luckily, we don't need anything near 16 hours.

###Downloading the Heroku toolbelt

Once you create and account and are sitting at the dashboard, you need to create a new app. Name the app, and then we'll need to download the heroku toolbelt.

https://toolbelt.heroku.com/

Use the version corresponding to your OS. After installing the toolbelt you can follow the directions given on the new app page. 

When initializing the Git repository, you need to cd (change directory) to the folder GameDealBot is in. For those who are familiar with Git, you can git clone, and use that folder. Those who have no idea what Git are, you can download the zip from this repository, and unzip it and use the folder that contains main.py as the directory for the repository.

After the command:

    git push heroku master

The app is now deployed to heroku and will do it's initial run. The last thing that needs to be done is to set up the scheduler.

###Adding a scheduler

Next we go to the Overview tab on the top left of our app page. There, under the "Installed Add-ons" section, we will click configure add-ons. There will be a search bar that says "Quickly add add-ons from Elements". Type in 'heroku scheduler' and choose it when it shows up. Once it is added, we need to tell it what to run.

Click the Heroku Scheduler title (it's a link) and it'll give you a new page where you can add a new job. Click add new job. In the $ box, we enter:

    python main.py
    
This tells it to run our main python file. Keep the dyno size at free, and set frequency to 10 minutes, hit save and we're done!
    
