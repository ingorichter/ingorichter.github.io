+++
categories = [""]
date = "2025-05-18T22:20:46-07:00"
description = "It's easy to virtualize macOS or Linux on a modern Mac"
draft = true
id = "1c9ed65eaad4f81d43920ed1320bf89b54e13a82"
link = ""
tags = ["TIL"]
title = "Running VMs on macOS"
+++

Running VMs (Virtual Machines) on a modern Mac with some Open Source Tools enables exploration and experimentation without sacrificing any production machine.

<!--more-->

## running-vms-on-macos

I was working on my ansible scripts in the past couple of days. I made some changes to accommodate a new Mac Mini that is sitting here for quite some time. It's the replacement machine for my aging Hackintosh. Anyway, when running ansible it would be great to run a couple of task on the destination machine. Since my ansible skills are very basic, I do a lot of trial and error along the way. Some tasks fail and others work. Some install software and tweak system settings and leave the new machine in an unfinished state. Ansible works great to automate the setup of machines or keep existing machines in sync with whatever change is requested by the ansible scripts. That works by expecting the target machine to be in a specific state. Let's say, I want to install Zen Browser on my new machine, then Ansible checks if Zen Browser is installed. If this is not the case, then it will install it. Running the same task again, will find the installed Zen Browser and does nothing. Perfect. But there is not way in Ansible, at least none that I know off, to remove or revert any applied tasks. This can leave the target machine in the said twilight state with half baked changes and installed software.

Ansible has was way to do a dry run, but this is not exactly the same and can produce, since it's not really taking any action on the target machine. Changing permissions or running any program on the target machine can hide problems that will be obvious once you run it for real. But enough of Ansible. This was my motivation to find a way to setup a macOS VM and test the Ansible scripts there. If the VM is crewed up, I can delete it and spin up a new copy. Easy peasy

## What OSS Software is available

I was experimenting with UTM and VirtualBuddy

