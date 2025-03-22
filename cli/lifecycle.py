from kitecore.lifecycle import rest_cycle

class LifecycleCLI:
    def __init__(self, subparsers):
        rest_parser = subparsers.add_parser("rest", help="Reset pyramids for a specific story")
        rest_parser.add_argument("--story", required=True, help="Name of the story to reset pyramids for")
        rest_parser.set_defaults(func=self.handle_rest)

    def handle_rest(self, args):
        rest_cycle(args.story)  # ✅ FIX: pass only the story string
