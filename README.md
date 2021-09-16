## Quick Start

In case that a problem arise to install the nltk-data, try this on a Python console:

``` python
import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()

```
###### To get started

**first** clone the repository into your project.
One of the easiest ways to get started is to **run the docker image** :

```
docker image build -t chatbot .  
```

## How it works

