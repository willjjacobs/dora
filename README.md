This is the repository for the DORA project. Very much a work in progress at this point.

In order to utilize this code:

Our project is designed to utilize Python version 3.5 or greater. A number of dependencies are specified and will be installed with a Pipfile or can be installed manually by referencing requirements.txt. Additionally, a webcam is required.

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
[~/Projects/dora] $ source /home/will/.local/share/virtualenvs/dora-TLaQji9E/bin/activate
[~/Projects/dora] $ python dora
```

Alternatively, a requirements.txt file is included and the requirements can be installed via
```bash
$ pip3 -r requirements.txt
```

To run Dora when at the top level directory:
```bash
[~/Projects/dora] $ ls
dora  Pipfile  README.md  requirements.txt  setup.py
[~/Projects/dora] $ python dora
....
```

At this point, our dashboard will open. Some debugging will be output to the console. After the dashboard window opens, it may take some time for the video feed to appear on the right hand side as the neural net initializes and then begins to interpret frames.