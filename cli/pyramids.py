from cli.cli_command import CLICommand
from lib.database import get_database
from lib.models import MemoryPyramid

class PyramidsCLI(CLICommand):
    def __init__(self, subparsers):
        self.register(subparsers)

    def register(self, subparsers):
        self.parser = subparsers.add_parser("pyramids", help="Manage memory pyramids")
        self.parser.add_argument("action", choices=["list"], help="Action to perform")
        self.parser.set_defaults(func=self.handle_command)

    def handle_command(self, args):
        db = get_database()
        session = db.Session()

        if args.action == "list":
            pyramids = session.query(MemoryPyramid).all()
            for pyramid in pyramids:
                print(f"{pyramid.id}: {pyramid.theme}")

        session.close()