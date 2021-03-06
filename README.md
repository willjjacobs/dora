This is the repository for the DORA project. Very much a work in progress at this point.

To start Dora server and client, issue the following commands from Dora's root directory:

`python dora server`

When `running server...` is displayed you may enter the next command:

`python dora client`

(opens in a new window, it will take a while for the image to appear)

Unfortunately, there is a bug in Dora Server where the HTTP server is running in its own thread it is not responsive to CTRL-C. Therefore, the user will have to kill the python processes using the terminal command `pkill` in Linux and MacOS. Windows users can just close the terminal windows. This will be fixed in later iterations.

Testing:

Before testing, be sure issue the command `pip install pytest pytest-cov pytest-pythonpath` to install the PyTest module and necessary plugins.

To run the tests, issue the command `pytest` from the project root directory. To run the tests and output code coverage statistics, `pytest --cov`.

We utilize PyTest as it allows for automatically collecting test files in our project and executing them. Configuration for running the tests as well as coverage reports is customized in setup.cfg. PyTest offers decorators to mark whether we expect a test to pass or fail and behave appropriately. Additionally, unit test functions can be parameterized if we know how we expect them to behave. Timeouts are useful due to the infinite networking aspect of our code.

Further plugins we may use would be linting plugins such as flake8, pyflakes, yapf, etc. which could be used to enforce code style as well as help police for unused imports and functions ensuring overall higher code quality. Another plugin we have been experimenting with is `pytest-pyqt`, which will allow for unit testing of the UI code. At current, we do not feel as though the unit tests we have written for our UI perform any useful function than running the actual application.

Plugins also exist to facilitate regression testing, data generation, race conditions and a multitude of other functions.

In order to utilize this code:

Our project is designed to utilize Python version 3.5 or greater. A number of dependencies are specified and will be installed with a Pipfile or can be installed manually by referencing requirements.txt. Additionally, a webcam is required.

Installing Python dependencies and utilizing Virtual Environments can be complex and difficult to debug. On occasion, it has been difficult to reproduce the environment. Below are strategies for installing our dependencies in either a virtual environment or system level.

Virtual Environment Setup:

Navigate to the top level dora directory once cloned.
This directory contains our module 'dora' as well a Pipfile and requirements.txt, which specifies our dependencies.
To read more about pipenv, look here: https://docs.pipenv.org/index.html

Pipenv will automatically install all of the required dependencies into a virtual environment.
To install pipenv and the required dependencies as well as run Dora, follow the below instructions:

```bash
[~/Projects/dora] $ pip install pipenv
[~/Projects/dora] $ pipenv install
Pipfile.lock not found, creating…
Locking [dev-packages] dependencies…
Locking [packages] dependencies…
Updated Pipfile.lock (2bd569)!
Installing dependencies from Pipfile.lock (2bd569)…
  🐍   ▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉▉ 23/23 — 00:00:07
To activate this project's virtualenv, run the following:
 $ pipenv shell
[~/Projects/dora] $ pipenv shell
Spawning environment shell (/bin/bash). Use 'exit' to leave.
source /home/will/.local/share/virtualenvs/dora-TLaQji9E/bin/activate
[~/Projects/dora] $ python dora
```
There are instances on Windows machines where python will crash when `python dora` is issues. This is an issue with the pipenv shell. Simply issue `exit` and then issue the command: `python dora`.

System Level Setup:

Alternatively, a requirements.txt file is included and the requirements can be installed via the command below:
```bash
$ pip3 -r requirements.txt
```
```
If you do not have system admin privileges pip can use the `--user` flag to install to the user's directory:
```bash
$ pip3 --user -r requirements.txt
```

To run Dora when at the top level directory:
```bash
[~/Projects/dora] $ ls
dora  Pipfile  README.md  requirements.txt  setup.py
[~/Projects/dora] $ python dora
....
```

At this point, our dashboard will open. Some debugging will be output to the console. After the dashboard window opens, it may take some time for the video feed to appear on the right hand side as the neural net initializes and then begins to interpret frames.

'''
pip3 install pipenv
pipenv --three
pipenv install [--dev]
'''

In order to run tests and coverage reports, use this command:
`pytest --cov=dora`

The following results will be displayed:
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

At this point, our dashboard will open. Some debugging will be output to the console. After the dashboard window opens, it may take some time for the video feed to appear on the right hand side as the neural net initializes and then begins to interpret frames.

