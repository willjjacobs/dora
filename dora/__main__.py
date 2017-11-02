"""
Entrypoint module for the entire DORA module
"""
import sys

if sys.version_info < (3, 5):
    print("You must use Python 3.5 or greater.")
    sys.exit(1)

from core import core
from dashboard.UI_Start import ui_main

def main():
  """
  Start point for the entire top level dora application.
  """
  ui_main(core.Core())
  #  # remove the first argument (dora)

if __name__ == '__main__':
  sys.exit(main())