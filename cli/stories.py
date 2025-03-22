# cli/stories.py

import argparse
import os
from kitecore import stories, pyramids
from lib.database import _Session
from lib.models import BaseMemory

class StoriesCLI:
    def __init__(self, subparsers: argparse._SubParsersAction):
        parser = subparsers.add_parser("stories", help="Manage story entries")
        story_subparsers = parser.add_subparsers(dest="stories_command", help="Story commands")

        # Add story command
        add_parser = story_subparsers.add_parser("add", help="Add a new story from file")
        add_parser.add_argument("--name", required=True, help="Unique name for the story")
        add_parser.add_argument("--file", required=True, help="Path to the story text file")
        add_parser.set_defaults(func=self.handle_add)

        # List stories command
        list_parser = story_subparsers.add_parser("list", help="List all stories")
        list_parser.set_defaults(func=self.handle_list)

        # Dump story info command
        dump_parser = story_subparsers.add_parser("dump", help="Dump full story and pyramid data to file")
        dump_parser.add_argument("--name", required=True, help="Name of the story to dump")
        dump_parser.add_argument("--out", required=True, help="Output file path")
        dump_parser.set_defaults(func=self.handle_dump)

    def handle_add(self, args):
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                story_text = f.read()
            story_id = stories.add_story(name=args.name, story_text=story_text)
            print(f"Story '{args.name}' added with ID {story_id}.")
        except Exception as e:
            print(f"Error: {e}")

    def handle_list(self, args):
        all_stories = stories.list_stories()
        if not all_stories:
            print("No stories found.")
        for s in all_stories:
            print(f"Story: {s['name']}\n  ID: {s['id']}\n")

    def handle_dump(self, args):
        story = None
        all_stories = stories.list_stories()
        for s in all_stories:
            if s['name'] == args.name:
                story = s
                break

        if not story:
            print(f"Error: Story with name '{args.name}' not found.")
            return

        # Fetch full content from DB directly
        session = _Session()
        try:
            story_data = session.query(BaseMemory).filter_by(id=story['id']).first()
            if not story_data:
                print(f"Error: Story data not found in DB for ID {story['id']}")
                return

            output_lines = [f"Story: {story['name']}\nID: {story['id']}\n\n{story_data.content}\n\n"]

            story_pyramids = pyramids.get_pyramids(story['id'])
            for pyramid in story_pyramids:
                output_lines.append(f"Pyramid ID: {pyramid['id']}\nTheme: {pyramid['theme']}\n")
                for level in pyramid['levels']:
                    output_lines.append(f"\n[Level {level['level']}]\n{level['content']}\n")
                output_lines.append("\n" + ("=" * 40) + "\n")

            with open(args.out, 'w', encoding='utf-8') as f:
                f.writelines([line + "\n" for line in output_lines])
            print(f"Dumped story and pyramid info to {args.out}")
        except Exception as e:
            print(f"Error during dump: {e}")
        finally:
            session.close()