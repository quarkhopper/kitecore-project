import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from cli.prompts import PromptsCLI
from cli.pyramids import PyramidsCLI
from cli.stories import StoriesCLI
from cli.lifecycle import LifecycleCLI  # ✅ Correctly registered CLI logic

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Kitecore CLI")
        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        self.prompts_cli = PromptsCLI(self.subparsers)
        self.pyramids_cli = PyramidsCLI(self.subparsers)
        self.stories_cli = StoriesCLI(self.subparsers)
        self.lifecycle_cli = LifecycleCLI(self.subparsers)  # ✅ This handles 'rest'

    def run(self):
        args = self.parser.parse_args()
        if not args.command:
            self.parser.print_help()
            sys.exit(1)

        args.func(args)

if __name__ == "__main__":
    CLI().run()
