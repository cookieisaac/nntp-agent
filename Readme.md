# NNTP Agent

A flexible news collection agent based on NNTP protocol

## Usage

```
python newsagent.py
```

## Core Code

```python
import nntplib
#Get a free server from http://www.freeusenetnews.com/
server = nntplib.NNTP("news.gmane.org")
server.list()
server.group('gmane.comp.python.committers')
```

## Bonus: Git Merge Conflict

### Q: Why I cannot push my code?
```
# git push origin master
Username for 'https://github.com': cookieisaac
Password for 'https://cookieisaac@github.com':
To https://github.com/cookieisaac/nntp-agent.git
 ! [rejected]        master -> master (fetch first)
error: failed to push some refs to 'https://github.com/cookieisaac/nntp-agent.git'
hint: Updates were rejected because the remote contains work that you do
hint: not have locally. This is usually caused by another repository pushing
hint: to the same ref. You may want to first merge the remote changes (e.g.,
hint: 'git pull') before pushing again.
hint: See the 'Note about fast-forwards' in 'git push --help' for details.

```
**A**: As described [here](http://stackoverflow.com/a/10298391/3806343),  the message tells you,

Merge the remote changes (e.g. 'git pull')
Use git pull to pull the latest changes from the remote repository to your local repository. In this case, pulling changes will require a merge because you have made changes to your local repository.

I'll provide an example and a picture to explain. Let's assume your last pull from origin/branch was at Commit B. You have completed and committed some work (Commit C). At the same time, someone else has completed their work and pushed it to origin/branch (Commit D). There will need to be a merge between these two branches.
```
local branch:                         --- Commit C 
                                    /
                                   /
                                  /
origin/branch: Commit A ------ Commit B ---- Commit D
```
Because you are the one that wants to push, Git forces you to perform the merge. To do so, you must first pull the changes from origin/branch.
```
local branch:                         --- Commit C -- Commit E
                                    /               /           
                                   /               /             
                                  /               /               
origin/branch: Commit A ------ Commit B ---- Commit D 
```
After completing the merge, you will now be allowed to fast-forward origin/branch to Commit E by pushing your changes.

Git requires that you handle merges yourself, because a merge may lead to conflicts.


### Q:I made a few changes on Github and then I made a few change in local. How do I push my local change to a updated Github?


**A**: As suggested [here](https://githowto.com/resolving_conflicts), open the conlicted file, manually resolve the following part

```
<<<<HEAD
Conflict A
========
Conflict B
>>>>>ChangesetID
```

to 

```
Merged
```

Then 
```
git add lib/hello.html
git commit -m "Merged master fixed conflict."
```

### Q: What if I got the following message?
```
You have not concluded your merge (MERGE_HEAD exists).
Please, commit your changes before you can merge.
```

**A**: As illustrated [here](http://stackoverflow.com/a/11647899/3806343)

If your previous pull failed to merge automatically and went to conflict state. And the conflict wasn't resolved properly before the next pull.

1. Undo the merge and pull again.

	To undo a merge:

	`git merge --abort` [Since git version 1.7.4]

	`git reset --merge` [prior git versions]

2. Resolve the conflict.

3. Don't forget to add and commit the merge.

4. git pull now should work fine.


## Todo
1. UML
2. Test the regular expression for extrating news title and body from html