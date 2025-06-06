+++
categories = ["git"]
date = "2025-06-05T22:31:24-07:00"
description = "Simplify working with multiple git identities and contexts by automating the identity selection."
draft = false
id = "94d2351c647f08d22a8079dcff12bedf304b26eb"
link = ""
tags = ["TIL", "git"]
title = "Manage Multiple Git Identities With Conditional Includes"
[params]
  [[headerimage]]
    src = "A_digital_illustration_of_a_large_deciduous_tree_i.png"
    alt = "AI generated illustration of git"
    stretch = "horizontal"

+++
[1]: https://git-scm.com/docs/git-config.html#_conditional_includes "Conditional Includes"

<!--more-->

## Managing Multiple Git Identities with Conditional Includes

As developers, we often work across different contexts - personal projects, open source contributions, and work repositories. Each context might require a different Git identity (name, email, and signing key). Manually switching between these identities is error-prone and tedious.

In this post, I'll share how I've solved this problem using [Git's conditional includes feature][1], which has dramatically simplified my workflow and prevented embarrassing identity mix-ups.

## The Problem

When working across different repositories, you might need different identities:

- __Work repositories__: Your corporate email and signing key
- __Open source contributions__: Your personal email or a project-specific one
- __Personal projects__: Your personal identity

Without automation, you'd need to remember to run `git config` commands each time you switch contexts, which is both annoying and error-prone. And I usually forget to do it, resulting in commits with the wrong identity/email address.

## The Solution: Conditional Includes

Git offers a powerful feature called [conditional includes][1] that lets you include specific configuration files based on conditions like:

1. The path of the repository (`gitdir`)
2. The remote URL of the repository (`hasconfig:remote.*.url`)

This allows you to automatically apply the right identity based on where a repository is located or which remote it's connected to.

> The included configuration file can contain other things like name, email, and signing key. This is only what I'm using in my setup. But you can overwrite many of the git config options if you deem it necessary.

## My Setup

Here's how I've structured my Git identity management:

### 1. Base Configuration

My main `.gitconfig` has a default identity and sets `useConfigOnly = true` to prevent Git from guessing my identity:

```gitconfig
[user]
    useConfigOnly = true
    name = Ingo Richter
    email = ingo.richter+github@gmail.com
```

### 2. Separate Identity Files

I maintain separate files for different contexts:

- `~/.dotfiles/git/github.gitconfig` - Personal GitHub identity
- `~/.dotfiles/git/github-corp.gitconfig` - Work GitHub identity
- `~/.dotfiles/git/gitcorp.gitconfig` - Internal corporate Git identity

Each file contains the appropriate user settings:

```gitconfig
# Personal GitHub (~/.dotfiles/git/github.gitconfig)
[user]
    name = Ingo Richter
    email = ingo.richter+github@gmail.com
    signingkey = 47179020517973BE

# Work GitHub (~/.dotfiles/git/github-corp.gitconfig)
[user]
    name = Ingo Richter
    email = irichter@work.com
    signingkey = DA67F86E8421C7A5
```

### 3. Conditional Includes Based on Remote URLs

This is something that I've found out recently, after we moved some of our work repos to GHEC and some repos stayed on the hosted internal git instance.
Now, I had to distinguish between work.corp and github.com repos. But I also had some personal/open source repos that were also on github.com. Now, I had an issue with my identities, since the path-based conditional include didn't work anymore for me. I keep all my work-related repos in a directory `work`. But, now there were repos hosted on work.corp and github.com. I didn't wanted the github.com repos select my personal identity. So, I was looking for a way to find another way to automatically select the correct identity. And that is when Remote URLs came into the picture.

The most powerful approach is using remote URL patterns to determine identity:

```gitconfig
# Corporate GitHub repositories
[includeIf "hasconfig:remote.*.url:https://github.com/adobe/**"]
    path = ~/.dotfiles/git/github-corp.gitconfig

[includeIf "hasconfig:remote.*.url:git@github.com:adobe/**"]
    path = ~/.dotfiles/git/github-corp.gitconfig

# Personal GitHub (fallback for other github.com repos)
[includeIf "hasconfig:remote.*.url:https://github.com/**"]
    path = ~/.dotfiles/git/github.gitconfig

[includeIf "hasconfig:remote.*.url:git@github.com:*/**"]
    path = ~/.dotfiles/git/github.gitconfig

# Internal corporate Git
[includeIf "hasconfig:remote.*.url:https://work.corp/**"]
    path = ~/.dotfiles/git/gitcorp.gitconfig
```

### 4. Path-Based Fallbacks

The path-based approach works perfectly for my personal projects. Since they reside in a separate directory, the identity switch doesn't need to consider any remote repositories.

However, if there are any other repositories in `~/develop/work/repos` that don't match any of the remote repository checks, the `github-corp.gitconfig` will be selected.

```gitconfig
[includeIf "gitdir:~/develop/fun/"]
    path = ~/.dotfiles/git/github.gitconfig

[includeIf "gitdir:~/develop/work/repos/"]
    path = ~/.dotfiles/git/github-corp.gitconfig
```

## Bonus: Identity Switching Command

Before I've learnt about the conditional include, I've created a Git alias to manually switch identities when needed:

```gitconfig
[alias]
    identity = "! git config user.name \"$(git config user.$1.name)\"; git config user.email \"$(git config user.$1.email)\"; git config user.signingkey \"$(git config user.$1.signingkey)\"; :"
```

This lets me run `git identity work` or `git identity personal` to switch profiles.

## Important Notes

1. __Order matters__: Git processes conditional includes in order, with later matches overriding earlier ones.
2. __Remote URL patterns__ (`hasconfig`) require Git 2.36+.
3. __Path patterns__ (`gitdir`) are processed before remote URL patterns.
4. Set `useConfigOnly = true` to prevent Git from guessing your identity.

## Conclusion

This setup has saved me countless hours and prevented embarrassing identity mix-ups. The best part is that it's completely automatic - I clone a repo, and Git automatically applies the right identity based on its location or remote URL.

For developers working across multiple contexts, I highly recommend setting up conditional includes to manage your Git identities. It's a small investment that pays off every day.

---

I hope this helps you out in some way. How do you manage multiple Git identities? Let me know in the comments!

Thanks for reading
Mahalo 🌸
