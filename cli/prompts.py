from cli.cli_command import CLICommand
from lib.database import get_database
from lib.models import PromptTemplate

class PromptsCLI(CLICommand):
    def __init__(self, subparsers):
        self.register(subparsers)

    def register(self, subparsers):
        self.parser = subparsers.add_parser("prompts", help="Manage prompt templates")
        self.parser.add_argument("action", choices=["list", "add"], help="Action to perform")
        self.parser.add_argument("--name", help="Prompt name (for 'add' action)")
        self.parser.add_argument("--template", help="Prompt template (for 'add' action)")
        self.parser.set_defaults(func=self.handle_command)

    def handle_command(self, args):
        db = get_database()
        session = db.Session()

        if args.action == "list":
            prompts = session.query(PromptTemplate).all()
            for prompt in prompts:
                print(f"{prompt.id}: {prompt.name} - {prompt.purpose}")

        elif args.action == "add":
            if not args.name or not args.template:
                print("Error: --name and --template are required for 'add' action")
                return

            new_prompt = PromptTemplate(name=args.name, template=args.template)
            session.add(new_prompt)
            session.commit()
            print(f"Added new prompt: {args.name}")

        session.close()