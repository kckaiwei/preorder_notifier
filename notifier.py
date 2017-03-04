import os, praw, time
from config import *


class Notifier(object):
    """Notifier class that compiles all methods and sends notification messages"""
    def __init__(self):
        if not os.path.isfile("config.py"):
            print "user config missing"
            exit(1)

        self._username = REDDIT_USERNAME
        self._password = REDDIT_PASS
        self._email_username = EMAIL_USERNAME
        self._email_password = EMAIL_PASSWORD
        self._to_address = TO_ADDRESS
        self._keyphrase_list = list()

        self._user_agent = ("Preorder-notifier 1.0")
        self._reddit_reader = praw.Reddit(user_agent=self._user_agent)
        self._reddit_reader.login(self._username, self._password, disable_warning=True)

    def add_keyphrase(self, keyphrase, subreddit, post_limit=50):
        """
        Adds a keyphrase dictionary set
        :param keyphrase: phrase being searched for
        :param subreddit: list of subreddits
        :param post_limit: how many posts to check
        :return:
        """
        phrase_dict = dict()
        phrase_dict['keyphrase'] = str(keyphrase)
        phrase_dict['subreddit'] = str(subreddit)
        try:
            phrase_dict['post_limit'] = int(post_limit)
        except TypeError:
            print "Post Limit provided was not an integer"
        self._keyphrase_list.append(phrase_dict)

    def _check_keyphrases(self):
        """
        Checks each keyphrase set in their respective subreddit
        :return:
        """
        if not os.path.isfile("posts_checked.txt"):
            posts_checked = []

        else:
            with open("posts_checked.txt", "r") as f:
                posts_checked = f.read()
                posts_checked = posts_checked.split("\n")
                posts_checked = filter(None, posts_checked)

        for keyphrase_dict in self._keyphrase_list:
            for subreddit in keyphrase_dict['subreddit']:
                sr = self._reddit_reader.get_subreddit(subreddit)
                for submission in sr.get_new(limit=keyphrase_dict['post_limit']):
                    if submission.id not in posts_checked:
                        posts_checked.append(submission.id)
                        if submission.title:
                            if keyphrase_dict['keyphrase'].lower() in submission.title.lower():
                                title = submission.title.encode('utf-8')
                        if submission.url:
                            url = submission.url.encode('utf-8')
                        self._notify(title, url)
                        print title
                        print url

        with open("posts_checked.txt", "w") as f:
            for post_id in posts_checked:
                f.write(post_id + "\n")

    def _notify(self, title, url=None):
        """
        Sends an email
        :param title: title of submission to send
        :param url: url of submission to send
        :return: True on success
        """
        import smtplib
        import email.mime.text

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(self._email_username, self._email_password)

        msg = email.mime.text.MIMEText(title, _charset="utf-8")
        server.sendmail(self._email_password, self._to_address, msg.as_string())
        server.quit()
        print title, "sent!"

    def start_continuous(self, interval_sec=60):
        while True:
            self._check_keyphrases()
            time.sleep(interval_sec)

    def start_once(self):
        self._check_keyphrases()
        pass

if __name__ == "__main__":
    n = Notifier
    n.add_keyphrase('Breath of the Wild Special Edition preorder', ['nintendoswitch', 'zelda'], 50)
    n.start_once()