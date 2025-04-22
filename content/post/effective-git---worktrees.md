+++
author = "Ingo Richter"
date = "2017-05-10T21:19:27-07:00"
categories = ["Git", "Programming"]
tags = ["Git", "Programming", "Tips", "Tricks", "Tools", "TIL"]
title = "Effective Git - Worktrees"
description = "Worktrees can save time switching between different feature branches"
draft = false
+++

You know this situation: you are working on new feature branch of your product. A bunch of files has been changed, nothing has settled yet and lots of uncommitted changes. This is how work in progress looks like. Everything could be alright, but then you are asked to check out that high priority issue that a customer reported.

What I did in this situation

- stash my changes with `git stash save` and provide a meaningful message for when I have to unstash- my changes
- changes branches and pull from master
- build the product
- repro the issue
- create a new branch for the fix
- implement the fix and push to the newly created branch
- let somebody else verify the fix
- go back to my previous branch
- `git stash pop` my work in progress
- continue working on the feature

# Introducing Worktrees

I was reading git release notes, and I stumbled upon something I haven’t heard before in the git context: worktree. It’s not a new feature. It was introduced back in 2015, but I discovered it a couple of weeks ago. It reminded me of the time when I used Perforce, and I had to create a Workspace for everything I was working on (okay, it wasn’t that bad).

The help for `git help worktree` gives you a very short summary of some operations available for worktrees.

{{< highlight bash "title=git-worktree">}}
NAME
       git-worktree - Manage multiple working trees

SYNOPSIS
       git worktree add [-f] [--detach] [--checkout] [--lock] [-b <new-branch>] <path> [<branch>]
       git worktree list [--porcelain]
       git worktree lock [--reason <string>] <worktree>
       git worktree prune [-n] [-v] [--expire <expire>]
       git worktree unlock <worktree>
{{< /highlight >}}

Sounds interesting to me. Let’s check it out.

IMHO worktrees have a couple of advantages over another git clone:

- less space wasted with another clone of the same repo
- easier to compare files between different worktrees
- work on multiple branches of the same repo without the hassle of messing everything up when switching branches (this happened a lot for me in the past)

> BTW: the current project directory is a worktree too.

There might be other good solutions to support that sort of workflows. Git is versatile and powerful. It has a lot to offer, and there are so many different ways to achieve the same result. Worktrees are a great addition, and they make good sense. Your mileage may vary.

Thanks for reading!

Feel free to share, leave a comment or ignore it.
