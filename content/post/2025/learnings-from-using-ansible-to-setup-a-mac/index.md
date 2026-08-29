+++
categories = ["TIL"]
date = "2025-06-01T22:40:26-07:00"
description = ""
draft = true
id = "50da383f7aa606ddca7818a7ce4c39e82d183dc5"
link = ""
tags = ["TIL"]
title = "Learnings From Using Ansible to Setup a Mac"
+++

<!--more-->
Setup a new mac with Ansible. I was hoping to have a solution that doesn't require any manual interaction after installing the OS, creating a new user, enable ssh and transfer the ssh key to the new machine to allow ssh without having to provide credentials when running Ansible.

## learnings-from-using-ansible-to-setup-a-mac

Sigh, I was not successful achieving this goal

- let me know if there is anything that can be improved
- running python3 will trigger the intallation the CLT and opens a confirmation dialog on the mac
- I've spent too much time trying to solve all the obstacles along the way. At some point, I caved and accepted my fate that I will have to install certain things manually or don't depend the python3 version that comes with macOS