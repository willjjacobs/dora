"""
Entrypoint module for the entire DORA module
"""
import sys
#from core import cli
#from dashboard.UI_Start import ui_main

def main():
  """
  Start point for the entire top level dora application.
  """
  if sys.version_info < (3, 5):
    print("You must use Python 3.5 or greater.")
    sys.exit(1)
  
  # Must be imported after that (for now?)
#  from core import cli
  from dashboard.UI_Start import ui_main
  
  if (len(sys.argv) > 1): #sys.argv[1] == "dashboard"):
    try:
      ui_main()
    except QXcbConnection:
      print("Must have a graphical window available.")
      sys.exit(1)
  else:
    cli.main(sys.argv[1:]) # remove the first argument (dora)
  print('Exiting the dora top level module')

if __name__ == '__main__':
  sys.exit(main())