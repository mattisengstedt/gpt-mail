from enum import Enum

GMAIL_ACCOUNT = "namn@gmail.com"
GMAIL_APP_PASSWORD= "ABC"
SLACK_ACCOUNT = "@ANVÄNDARNAMN"
OPENAI_API_KEY = "APINYCKEL"
SLACK_BOT_TOKEN = "SLACK BOT TOKEN"

class EmailCategory(Enum):
    NEWSLETTER = ("Nyhetsbrev", False, False)
    PRIORITY = ("Prioriterat", True, True)
    MEETING = ("Möten & inbjudningar", False, True)
    ORDER = ("Order & fakturor", False, False)
    SUPPORT = ("Support & kundservice", False, True)
    WORK = ("Jobbrelaterat", True, True)
    REMINDER = ("Påminnelser & deadlines", False, True)
    SYSTEM = ("Automatiserade systemnotiser", False, False)
    OTHER = ("Övrigt", False, False)

    def __init__(self, label, summarize, needs_reply):
        self.label = label
        self.should_summarize = summarize
        self.might_need_reply = needs_reply

    @property
    def summarize(self):
        return self.should_summarize

    @property
    def needs_reply(self):
        return self.might_need_reply
