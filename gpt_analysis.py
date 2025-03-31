import openai
import user_settings
import email_processing

# OpenAI API-nyckel
client = openai.Client(api_key=user_settings.OPENAI_API_KEY)

# Kategorier
categories = [
    "Nyhetsbrev", "Prioriterat", "Möten & inbjudningar", "Order & fakturor",
    "Support & kundservice", "Jobbrelaterat", "Påminnelser & deadlines",
    "Automatiserade systemnotiser", "Övrigt"
]

def map_gpt_output_to_category(label: str) -> user_settings.EmailCategory:
    for category in user_settings.EmailCategory:
        if category.label.lower() == label.strip().lower():
            return category
    return user_settings.EmailCategory.OTHER

# Funktion för att analysera och kategorisera e-post
def categorize_email(sender, subject, body):
    prompt = f"""
    Kategorisera detta e-postmeddelande i en av följande kategorier:
    {', '.join(categories)}.

    E-post:
    Avsändare: {sender}
    Ämne: {subject}
    Innehåll: {body}

    Returnera endast kategorin.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    raw_label = response.choices[0].message.content.strip()
    return map_gpt_output_to_category(raw_label)


# Funktion för att generera en kort sammanfattning av jobbrelaterade och prioriterade mejl
def summarize_email(sender, subject, body):
    prompt = f"""
    Sammanfatta detta e-postmeddelande mycket kortfattat, max 2 meningar.

    E-post:
    Avsändare: {sender}
    Ämne: {subject}
    Innehåll: {body}

    Returnera endast sammanfattningen.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()


# Funktion för att avgöra om ett svar förväntas och generera ett förslag på svar
def generate_reply(sender, subject, body, to_field, cc_field):
    # Kontrollera om din e-postadress finns i "To" eller "Cc"
    if email_processing.EMAIL_ACCOUNT.lower() not in to_field.lower() and email_processing.EMAIL_ACCOUNT.lower() not in cc_field.lower():
        return "Ingen respons behövs."

    prompt = f"""
    Avgör om detta e-postmeddelande förväntar sig ett svar från mottagaren ({email_processing.EMAIL_ACCOUNT}). 
    Om det gör det, generera ett kort och artigt svar.

    E-post:
    Avsändare: {sender}
    Mottagare: {to_field}
    Kopia: {cc_field}
    Ämne: {subject}
    Innehåll: {body}

    Returnera antingen:
    - "Ingen respons behövs." om ingen åtgärd krävs.
    - Ett förslag på svar om det förväntas.
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()