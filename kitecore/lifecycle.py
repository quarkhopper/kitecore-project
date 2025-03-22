# kitecore/lifecycle.py

from kitecore import pyramids, stories

def rest_cycle(story_name: str) -> None:
    """
    Resets the state by deleting all pyramids related to the specified story
    and regenerating one unconstrained and one themed pyramid per extracted theme.
    """
    print(f"[REST] Fetching story: {story_name}...")
    story = None
    all_stories = stories.list_stories()
    for s in all_stories:
        if s['name'] == story_name:
            story = s
            break

    if not story:
        print(f"[REST] Story with name '{story_name}' not found.")
        return

    print(f"[REST] Deleting all existing pyramids related to '{story_name}'...")
    count = pyramids.delete_all_pyramids_for_story(story_name)
    print(f"[REST] {count} pyramid(s) related to '{story_name}' deleted.")

    print(f"[REST] Extracting themes from original story...")
    themes = pyramids.extract_themes(story['id'])
    print(f"[REST] Extracted themes: {themes}")

    print(f"[REST] Generating unconstrained pyramid...")
    pyramids.generate_pyramid(story['id'])

    for theme in themes:
        print(f"[REST] Generating pyramid for theme: {theme}...")
        pyramids.generate_pyramid(story['id'], seed_theme=theme)

    print("[REST] Rest cycle complete.")
