import argparse
import sys

class PrintVersion(argparse.Action):
    """
    Print versions of modules, apis and everything we pull in for easier debugging
    """

    print("Important version information should be printed here!")

    def __call__(self, parser, namespace, values, option_string=None):
        sys.exit(0)


def main(argv=None):
    """
        Commandline interface for the meta-templating engine
    """

    cli = argparse.ArgumentParser(
        "meta-templating",
        description=("free meta-templating engine for overlays")
    )

    cli.add_argument("--version", "-V", nargs=0, action=PrintVersion,
                     help="print version info and exit")
    cli.add_argument("--devmode", action="store_true",
                     help="force-enable development mode")
    cli.add_argument("--verbose", "-v", action='count',
                     default="high",
                     help="increase verbosity")
    cli.add_argument("--quiet", "-q", action='count', default=0,
                     help="decrease verbosity")


if __name__ == '__main__':
    print("Hello, welcome to our meta-templating engine!")

    sys.exit(main())
