"""
Entrypoint module for the entire DORA module
"""
import sys

if sys.version_info < (3, 5):
    print("You must use Python 3.5 or greater.")
    sys.exit(1)

def main(args = sys.argv):
    """
    Start point for the entire top level dora application.
    """

    if (len(args) >= 2):
        if (args[1] == 'server'):
            import core.core
            c = Core()
        if (args[1] == 'client'):
            from dashboard.UI_Start import ui_main
            ui_main()
        else:  # (len(sys.argv) > 2):
            print("Sample usage: \n"
                  "To launch the dashboard: python dora client\n"
                  "To launch the server: python dora server\n"
                  "To launch both on localhost: python dora\n")
            return 1
    else:
        print("You must utilize two separate terminals")
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())