import praw
import os
from config_bot import *
from _codecs import encode

def login():
    """Logins to reddit, returns praw.reddit"""
    if not os.path.isfile("config_bot.py"):
        print "user config missing"
        exit(1)

    user_agent = ("Game Deal Checker 1.0")
    r = praw.Reddit(user_agent=user_agent)

    r.login(REDDIT_USERNAME, REDDIT_PASS, disable_warning=True)

    return r


def run(r, posts):
    """Body function"""
    if not os.path.isfile("posts_checked.txt"):
        posts_checked = []

    else:
        with open("posts_checked.txt" , "r") as f:
                posts_checked = f.read()
                posts_checked = posts_checked.split("\n")
                posts_checked = filter(None, posts_checked)

    subreddit = r.get_subreddit('gamedeal')
    for submission in subreddit.get_hot(limit=posts):
        if submission.id not in posts_checked:
            if submission.score >= score_limit:
                posts_checked.append(submission.id)
                if submission.title:
                    title = submission.title.encode('utf-8')
                if submission.url:
                    url = submission.url.encode('utf-8')
                email(title, url)
                print title
                print url

    with open("posts_checked.txt" , "w") as f:
        for post_id in posts_checked:
            f.write(post_id + "\n")

def email(title, url):
    """email function to email to text message"""
    import smtplib
    import email.mime.text

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(EMAIL_USERNAME, EMAIL_PASSWORD)

    print title

    msg = email.mime.text.MIMEText(title, _charset = "utf-8")
    server.sendmail(EMAIL_USERNAME, TO_ADDRESS, msg.as_string())
    server.quit()
    print "sent!"

if __name__ == "__main__":
    """Start of bot"""
    print "running"
    score_limit = SCORE_LIMIT
    run(login(), POST_LIMIT)
    print "exiting"
