# Instagram Bot

A simple Instagram bot that cycles through hashtags listed at a file and automatically likes pictures with those hashtags to get more followers.

Developed in Python and built with the mechanize library

## Setup

At first, get the source. Clone this repository:

    $ git clone https://github.com/quasiyoke/InstaBot.git

### Requirements

You can install all needed requirements with single command:

    $ pip install -r requirements.txt

### Configuration

Create `configuration.yml` file containing your information, e.g.:

```yaml
CREDENTIALS:
  LOGIN: "your_login"
  PASSWORD: "topsecret"
SLEEPTIME: 5
PERHASHTAG: 10
```

The format for `hashtags.txt` file is to have each hashtag seperated by line, e.g.:

```
I
Love
Python
```
## Launching

Run:

    $ python InstaBot.py
