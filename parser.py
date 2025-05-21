
import spacy
import subprocess
import importlib.util
import re
import dateparser

def load_spacy_model():
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"], check=True)
        return spacy.load("en_core_web_sm")

nlp = load_spacy_model()


DAYS = {
    "monday": "Monday",
    "tuesday": "Tuesday",
    "wednesday": "Wednesday",
    "thursday": "Thursday",
    "friday": "Friday",
    "saturday": "Saturday",
    "sunday": "Sunday",
    "weekends": ["Saturday", "Sunday"],
    "weekdays": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}

def parse_availability(text):
    text = text.lower()
    doc = nlp(text)
    results = []

    for day_key, day_val in DAYS.items():
        if day_key in text:
            pattern = rf"{day_key}[^.,;]*"
            matches = re.findall(pattern, text)

            for match in matches:
                start, end = "10:00", "16:00"

                if "morning" in match:
                    start, end = "08:00", "12:00"
                elif "afternoon" in match:
                    start, end = "13:00", "17:00"
                elif "evening" in match:
                    start, end = "17:00", "20:00"
                elif "after" in match:
                    time_match = re.search(r"after (\d{1,2})(am|pm)?", match)
                    if time_match:
                        hour = int(time_match.group(1))
                        if time_match.group(2) == "pm" and hour != 12:
                            hour += 12
                        start = f"{hour:02d}:00"
                        end = "20:00"
                elif "all day" in match:
                    start, end = "08:00", "18:00"

                if isinstance(day_val, list):
                    for d in day_val:
                        results.append((d, start, end))
                else:
                    results.append((day_val, start, end))

    return results
