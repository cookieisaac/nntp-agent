# NNTP Agent

A flexible news collection agent based on NNTP protocol

## Core Code

```python
import nntplib
#Get a free server from http://www.freeusenetnews.com/
server = nntplib.NNTP("news.gmane.org")
server.list()
server.group('gmane.comp.python.committers')
```

## Todo
UML
