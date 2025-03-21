from lib.database import get_database
from lib.models import PromptTemplate
from sqlalchemy.orm import sessionmaker

# Get database session
db = get_database()
engine = db.get_engine()
Session = sessionmaker(bind=engine)
session = Session()

# Standard prompts to insert
prompts = [
    {"name": "condense", "purpose": "condensing unconstrained", "template": "Condense the following story to approximately [WORDCOUNT] words while preserving its core narrative, tone, and emotional depth. Retain the most essential details, character development, and key moments while eliminating redundant or less critical passages. Ensure the story remains engaging and thematically intact. Here is the story: [STORY]"},
    {"name": "condense_thematic", "purpose": "condensing thematic constraint", "template": "Condense the following story to approximately [WORDCOUNT] words, ensuring that the theme of '[THEME]' remains central. While reducing length, retain the story’s core narrative, tone, and emotional depth. Preserve key moments, character development, and essential details that reinforce the chosen theme. Remove redundant or less critical passages while enhancing the elements that contribute to the theme's presence and impact. The goal is to create a concise version of the story that still fully embodies its thematic essence. Here is the story: [STORY]"},
    {"name": "one_sentence", "purpose": "synopsis", "template": "Summarize the following story in a single, well-formed sentence that captures its core narrative, primary conflict, and resolution while maintaining its tone and emotional weight. Do not include unnecessary details. Here is the story: [STORY]"},
    {"name": "one_sentence_thematic", "purpose": "synopsis", "template": "Summarize the following story in a single, well-formed sentence that captures its core narrative, primary conflict, and resolution while maintaining its tone and emotional weight. Ensure that the theme of '[THEME]' is clearly reflected in the summary, emphasizing its influence on the story’s events, characters, and meaning. Do not include unnecessary details. Here is the story: [STORY]"},
    {"name": "extract_themes", "purpose": "theme_extraction", "template": "Analyze the following story and identify the 10 most significant one-word themes that capture its core concepts, emotions, and conflicts. The themes should be unique and reflect major narrative elements or underlying ideas. Present them as a single comma-separated list with no additional explanation. Here is the story: [STORY]"},
]

# Insert only if they don't exist
for prompt in prompts:
    exists = session.query(PromptTemplate).filter_by(name=prompt["name"]).first()
    if not exists:
        session.add(PromptTemplate(**prompt))

# Commit changes
session.commit()
session.close()

print("Standard prompts seeded successfully!")
