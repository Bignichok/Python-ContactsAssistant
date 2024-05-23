from prompt_toolkit.completion import Completer, Completion


class ContactCompleter(Completer):
    def __init__(self, command_args, book) -> None:
        super().__init__()
        self.command_args = command_args
        self.book = book

    def get_completions(self, document, complete_event):
        text = document.text
        words = text.split()

        if not words:
            for command in self.command_args:
                yield Completion(command, start_position=0)
        elif len(words) == 1:
            for command in self.command_args:
                if command.startswith(words[0]):
                    yield Completion(command, start_position=-len(words[0]))
        elif len(words) > 1:
            command = words[0]
            if command in self.command_args:
                if len(self.command_args[command]) >= len(words) - 1:
                    if (
                        self.command_args[command][len(words) - 2]
                        == "CONTACT_NAME".lower()
                    ):
                        for contactname in self.book.data.keys():
                            if contactname.startswith(words[1]):
                                yield Completion(
                                    contactname, start_position=-len(words[1])
                                )
