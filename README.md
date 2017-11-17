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

In order to run tests and coverage reports, use this command:
```bash
(dora-TLaQji9E) will@will-Falco:[~/Projects/dora] $ pytest --cov=dora
============================= test session starts =============================
platform linux -- Python 3.5.2, pytest-3.2.3, py-1.4.34, pluggy-0.4.0
rootdir: /home/will/Projects/dora, inifile: pytest.ini
plugins: cov-2.5.1
collected 4 items

dora/tests/env_test.py .s
dora/tests/neuralnet_test.py x
dora/tests/vision_test.py x

----------- coverage: platform linux, python 3.5.2-final-0 -----------
Name                                  Stmts   Miss Branch BrPart  Cover
-----------------------------------------------------------------------
dora/__init__.py                          1      0      0      0   100%
dora/__main__.py                          8      8      2      0     0%
dora/core/__init__.py                     0      0      0      0   100%
dora/core/core.py                        70     70      0      0     0%
dora/core/helpers.py                     25     25      0      0     0%
dora/core/neuralnet/NeuralNet.py         43     18      4      0    62%
dora/core/neuralnet/NeuralNetDTO.py       6      4      0      0    33%
dora/core/neuralnet/__init__.py           0      0      0      0   100%
dora/core/vision/__init__.py              0      0      0      0   100%
dora/core/vision/vision.py              113     76      6      0    31%
dora/dashboard/UI_Start.py              158    158      6      0     0%
dora/dashboard/__init__.py                0      0      0      0   100%
dora/dashboard/jsonsocket.py             75     75     20      0     0%
dora/dashboard/util.py                   45     45      2      0     0%
dora/tests/__init__.py                    0      0      0      0   100%
dora/tests/env_test.py                    7      1      0      0    86%
dora/tests/neuralnet_test.py             19      8      2      0    52%
dora/tests/vision_test.py                23     12      2      0    44%
-----------------------------------------------------------------------
TOTAL                                   593    500     44      0    15%


=============== 1 passed, 1 skipped, 2 xfailed in 3.25 seconds ================
```

Useful links:
 * https://docs.python.org/3/tutorial/modules.html
 * https://docs.python.org/3/distutils/setupscript.html
 * https://bitbucket.org/pyglet/pyglet/src/f48574e6c61c?at=default
 * https://github.com/django/django