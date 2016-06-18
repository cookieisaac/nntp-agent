#NNTP Agent

A flexible news collection agent based on NNTP protocol

## Core Code

```python
import nntplib
#Get a free server from http://www.freeusenetnews.com/
server = nntplib.NNTP("news-archive.icm.edu.pl")
server.list()
server.group('junk')
```