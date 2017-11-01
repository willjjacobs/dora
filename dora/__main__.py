"""
Entrypoint module for the entire DORA module
"""
import sys

if sys.version_info < (3, 5):
    print("You must use Python 3.5 or greater.")
    sys.exit(1)

from core.core import main as core_main
from dashboard.UI_Start import ui_main

def main():
  """
  Start point for the entire top level dora application.
  """
  if (len(sys.argv) > 1): #sys.argv[1] == "dashboard"):
    ui_main()
    # print("inside the top level if")
    # try:
    #   ui_main()
    # except QXcbConnection:
    #   print("Must have a graphical window available.")
    #   sys.exit(1)
  else:
    core_main(sys.argv[1:]) # remove the first argument (dora)
  print('Exiting the dora top level module')

if __name__ == '__main__':
  sys.exit(main())