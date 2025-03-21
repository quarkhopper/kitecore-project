import sys
import os

# Ensure the project root is in sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import argparse
from cli.prompts import PromptsCLI
from cli.pyramids import PyramidsCLI

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(description="Kitecore CLI")
        self.subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        self.prompts_cli = PromptsCLI(self.subparsers)
        self.pyramids_cli = PyramidsCLI(self.subparsers)

    def run(self):
        args = self.parser.parse_args()
        if not args.command:
            self.parser.print_help()
            sys.exit(1)
        
        args.func(args)

if __name__ == "__main__":
    CLI().run()
