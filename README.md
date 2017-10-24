This is the repository for the DORA project. Very much a work in progress at this point. Currently the setup.py is useless. 

Sample usage at the moment:
```bash
jacobsw@tux-49:[~/506/dora] $ python dora
Hello from the DORA module!
[]
Exiting the dora.core module cli
Exiting the dora top level module
jacobsw@tux-49:[~/506/dora] $ python dora more args for the cli
Hello from the DORA module!
['more', 'args', 'for', 'the', 'cli']
Exiting the dora.core module cli
Exiting the dora top level module
jacobsw@tux-49:[~/506/dora] $ cd dora
jacobsw@tux-49:[~/506/dora/dora] $ python core
[]
Exiting the dora.core module cli
jacobsw@tux-49:[~/506/dora/dora] $ python core more args
['more', 'args']
Exiting the dora.core module cli
jacobsw@tux-49:[~/506/dora/dora] $ 
```

Useful links:
 * https://docs.python.org/3/tutorial/modules.html
 * https://docs.python.org/3/distutils/setupscript.html
 * https://bitbucket.org/pyglet/pyglet/src/f48574e6c61c?at=default
 * https://github.com/django/django