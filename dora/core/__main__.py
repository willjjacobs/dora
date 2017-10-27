"""
Entrypoint module if dora.core is called from the command line.
"""

import sys
from cli import main

if __name__ == '__main__':
  sys.exit(main())