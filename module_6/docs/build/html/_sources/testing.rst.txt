Testing Guide
=============
Run all tests using:
``pytest -m "web or buttons or analysis or db or integration"``

Markers
-------
* ``web``: Flask route tests.
* ``buttons``: Busy-state logic.
* ``analysis``: Formatting checks.
* ``db``: Database operations.
* ``extras``: Extra coverage (100%).