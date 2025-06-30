import spacy

nlp = spacy.load("en_core_web_sm")

def is_foreign_law_question(text):
    doc = nlp(text)
    foreign_countries = {
        "India", "UK", "USA", "United States", "Canada", "Australia", "UAE", "Bangladesh",
        "Afghanistan", "Iran", "Iraq", "Saudi Arabia", "China", "Germany", "France", "Italy",
        "Russia", "Ireland", "Japan", "South Korea", "Brazil", "Mexico", "Spain"
    }
    for ent in doc.ents:
        if ent.label_ == "GPE":
            if ent.text.strip().lower() != "pakistan" and ent.text.strip() in foreign_countries:
                return True
    return False
