# ToyChord

ToyChord is an implementation of the
[Chord DHT](https://pdos.csail.mit.edu/papers/chord:sigcomm01/chord_sigcomm.pdf)
paper. It supports replication and two consistency flavors, namely
linearizability (through chain replication) and eventual consistency. Finger
tables are currently not incorporated.

## Setting up

Please follow the instructions in the [deployment](DEPLOYMENT.md) guide.

## Structure

- [Back End](backend): Chord DHT implementation as a REST API, written in
Python/Flask.
- [CLI Client](cli-client): A CLI tool written in Python (using `click` module)
that interfaces with the REST API.

Supplementary information is provided in the [architecture](ARCHITECTURE.md)
document.

## Authors

Alphabetically,

- [Angeliki Garoufalia](https://github.com/haanistik)
- [Filippos Malandrakis](https://github.com/fillmln)
- [Konstantinos Psychogios](https://github.com/KosPsych)
