# Deployment

## Installation

1. Install required packages

    ```bash
    $ sudo apt install python3 python3-pip python3-venv python3-testresources
    ```
    
2. Setup and activate a virtual environment:

    ```bash
    $ cd /path/to/ToyChord
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

5. Configure Chord functionality, navigating to `backend/utils/constants.py`

    ```bash
    BOOTSTRAP_NODE = "<BOOTSTRAP_IP>:<BOOTSTRAP_PORT>"
    RING_SIZE = pow(2, 160)
    REPLICATION_FACTOR = <REPLICATION_FACTOR>
    CONSISTENCY_MODE = "<CONSISTENCY_MODE>"
    ```

    , where:

    - `BOOTSTRAP_IP`: The IP address on which the bootstrap server will be
    listening.
    - `BOOTSTRAP_PORT`: The port the bootstrap server will be listening to.
    - `REPLICATION_FACTOR`: The number of replicas that will be stored in the
    ring for each key-value pair (positive integer).
    - `CONSISTENCY_MODE` = `{CHAIN_REPLICATION,EVENTUAL}`: The
    consistency mode under which the Chord DHT will operate.

## Usage

Fire up some Chord nodes (Flask servers ;p)

```bash
$ cd /path/to/ToyChord/backend
$ flask db upgrade
$ FLASK_APP=run.py flask run --host <IP> -p <PORT>
```

, where:

- `IP`: The IP address on which the server will be deployed.
- `PORT`: The port the server will be listening to.

**Important notes**:

1. Due to current setup limitations, for each Chord node a seperate copy
of the repo is required.

2. Bootstrap node must always be up and running when the Chord DHT is operated
(at the ip:port address configured during installation)

3. For `REPLICATION_FACTOR` equal to K, the ring must always have at least K
members.

---

You are now set :) You can submit commands to your homemade Chord DHT via the
cli-client you previously installed. To get started with it, try typing
`chord --help`.
