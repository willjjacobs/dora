"""
Entrypoint module for the entire DORA module
"""
import sys
from core import cli
from dashboard.UI_Start import ui_main

def open_ui():
  ui_main()

def main():
  print("Hello from the DORA module!")
  open_ui()
  cli.main(sys.argv[1:]) # remove the first argument (dora)
  print('Exiting the dora top level module')

if __name__ == '__main__':
  sys.exit(main())