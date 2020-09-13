+++
date = "2016-10-11T09:15:51-07:00"
draft = false
title = "TIL - SIGINFO is awesome"
tags  = [ "Notes", "Tips", "Programming", "shell", "bash", "cli"]
categories = [ "Tips", "Shell", "Bash" ]
+++

# TIL - SIGINFO is awesome

Today I learnt something really awesome. If you use a Unix based operating system, then you will be able to send any process a signal. This might be either `Ctrl+C` or **SIGINT** to interrupt that process. Or you can send **SIGINFO**  to report the progress of it's operation. Why this is awesome? Did you ever copy a huge amount of data and `cp` didn't tell you how much has data has been copied so far? **SIGINT** to the rescue.

[source, bash]
----
irichter@irichter-MacBookPro:~/Documents/Virtual Machines » cp -a dev-setup.vmwarevm dev-setup-2.vmwarevm

load: 2.02  cmd: cp 49102 uninterruptible 0.05u 2.28s
dev-setup.vmwarevm/dev-setup-61da15a0.vmem -> dev-setup-2.vmwarevm/dev-setup-61da15a0.vmem  32%

load: 2.02  cmd: cp 49102 uninterruptible 0.06u 4.11s
dev-setup.vmwarevm/dev-setup-61da15a0.vmem -> dev-setup-2.vmwarevm/dev-setup-61da15a0.vmem  74%
----

I send `Ctrl+T` two times to the cp process. In one case 32% of the data has been copied. In the other case 74%.

This will help especially with programs that don't have an option to report progress.