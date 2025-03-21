from abc import ABC, abstractmethod

class CLICommand(ABC):
    """Abstract base class for CLI commands."""

    @abstractmethod
    def register(self, subparsers):
        """Register the command with argparse."""
        pass