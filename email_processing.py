import imaplib
import email
from collections import defaultdict
import user_settings
from email.header import decode_header
import slack_notifier
import gpt_analysis

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = user_settings.GMAIL_ACCOUNT
EMAIL_PASSWORD = user_settings.GMAIL_APP_PASSWORD

# Funktion för att hämta och kategorisera olästa mejl
def process_unread_emails():
    # Anslut till Gmail IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
    mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)
    mail.select("inbox")

    # Sök efter endast olästa mejl
    status, messages = mail.search(None, '(UNSEEN)')
    email_ids = messages[0].split()
    email_ids.reverse()

    category_counts = defaultdict(int)
    total_unread = len(email_ids)
    summarized_emails = []
    replies = []

    for email_id in email_ids:
        status, data = mail.fetch(email_id, "(BODY.PEEK[])")  # Använd PEEK för att inte markera som läst
        raw_email = data[0][1]
        msg = email.message_from_bytes(raw_email)
        subject, encoding = decode_header(msg["Subject"])[0]
        subject = subject.decode(encoding or "utf-8") if isinstance(subject, bytes) else subject
        sender, encoding = decode_header(msg["From"])[0]
        sender = sender.decode(encoding or "utf-8") if isinstance(sender, bytes) else sender
        to_field = msg.get("To", "").strip()
        cc_field = msg.get("Cc", "").strip()

        # Extrahera e-posttext
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        # Anropa funktionen för att kategorisera e-post
        category = gpt_analysis.categorize_email(sender, subject, body)
        category_counts[category] += 1

        # Om mejlet är prioriterat eller jobbrelaterat, sammanfatta det
        if category.summarize:
            summary = gpt_analysis.summarize_email(sender, subject, body)
            summarized_emails.append((sender, subject, summary))

        # Kolla om svar förväntas och generera svarsförslag
        reply = gpt_analysis.generate_reply(sender, subject, body, to_field, cc_field)
        if category.needs_reply:
            replies.append((sender, subject, reply))

    # Stäng anslutningen
    mail.logout()

    output = f"📨 Totalt antal olästa mejl: {total_unread}\n"
    for category, count in category_counts.items():
        output += f"📌 {category.label}: {count}\n"

    if summarized_emails:
        output += "\n🔥 *Sammanfattning av prioriterade och jobbrelaterade mejl:*\n"
        for sender, subject, summary in summarized_emails:
            output += f"*{subject}* från {sender}\n> {summary}\n\n"

    if replies:
        output += "\n💬 *Förslag på svar:*\n"
        for sender, subject, reply in replies:
            output += f"*{subject}* från {sender}\n> {reply}\n\n"

    slack_notifier.send_slack_message(output)