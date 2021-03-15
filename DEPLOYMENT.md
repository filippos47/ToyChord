# Deployment

## Installation

1. Install required packages

    ```bash
    $ sudo apt install python3 python3-pip python3-venv python3-testresources
    ```
    
2. Setup and activate a virtual environment:

    ```bash
    $ cd /path/to/Toychord
    $ python3 -m venv .venv
    $ source .venv/bin/activate
    ```

3. Install pip requirements
    
    ```bash
    $ pip3 install -r requirements.txt
    ```

4. Install cli-client

    ```bash
    $ cd /path/to/ToyChord/cli-client
    $ python3 setup.py build
    $ python3 setup.py install
    ```

## Usage

Fire up some Chord nodes (Flask servers ;p):

```bash
$ cd /path/to/Toychord/backend
$ flask db upgrade
$ FLASK_APP=run.py flask run --host <IP> -p <PORT>
```

Parameters:

- IP: The IP address on which the server will be deployed.
- PORT: The port the server will be taking requests from.

Note: Due to current setup limitations, for each Chord node a seperate copy
of the repo is required.

And you are set :) You can submit commands to your homemade Chord DHT via the
cli-client you previously installed. To get started with it, try typing
`chord --help`.
