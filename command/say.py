from . import Command


class Say(Command):

    def get_name(self):
        return "say"

    def invoke(self, *args):
        # do the say command
        sentence = " ".join(args)
        return f"I said '{sentence}'"


if __name__ == "__main__":
    say = Say()
    print (say.invoke("some words"))
