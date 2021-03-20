# Architecture

## Backend

The REST API features the following primary endpoints:

- `/join`: Join Chord node to the ring
- `/depart`: Remove Chord node from the ring
- `/insert`: Insert key-value pair
- `/query`: Place query for either specific key or every entry
- `/delete`: Delete key-value entry for specified key
- `/overlay`: Show current ring topology

Some additional helper endpoints are implemented, not to be directly hit from
users/CLI:

- `/bootstrap/management`: Contact bootstrap node to inform about node arrival/
departure
- `/update_predecessor`: Inform Chord node to update its predecessor
- `/update_successor`: Inform Chord node to update its successor
- `/fix_replication`: Stabilise replica count in case of node arrival/departure

The directory structure is the following:

```bash
-- endpoints # Each API endpoint resides in a dedicated file
---- routes.py # Binds endpoints to urls
-- migrations # SQLite stuff
-- utils # Functionality used by the endpoints
-- models.py # Database schema configuration
-- app.py # Flask server configuration
-- database.py # SQLite initialization
-- run.py # Backend deployer
```

## CLI-client

The CLI client features one subprocessor for each primary API endpoint
described above, as well as a bulk-operation method for read/write operations.

The directory structure is the following:

```bash
-- cli # Actual CLI implementation
---- commands # CLI methods
---- utils # Functionality used by CLI methods
---- __main__.py # Binds various CLI methods to CLI interface
-- setup.{py,cfg} # Python packaging configuration
```
