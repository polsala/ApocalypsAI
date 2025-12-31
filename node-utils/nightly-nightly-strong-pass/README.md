Nightly Strong Pass
===================

A whimsical command-line utility that evaluates the strength of a password and provides friendly suggestions to make it stronger.

Installation
------------
npm install -g nightly-strong-pass

Usage
-----
nightly-strong-pass <password>

Example
-------
$ nightly-strong-pass P@ssw0rd!
Your password is moderately strong.
Suggestions:
- Add more symbols
- Increase length

How It Works
------------
The utility scores a password on a scale of 0–100 based on length, character variety, and randomness. It then outputs a friendly message and actionable suggestions.

License
-------
MIT
