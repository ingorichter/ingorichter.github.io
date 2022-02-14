+++
title = "Adding Multiple Files to Macos Gatekeeper"
categories = ["TIL", "macos", "security", "tips", "tricks"]
tags = ["TIL"]
date = 2022-02-10
draft = false
+++

## The Gatekeeper

Before I forget what I learned today, I better write it down.

Gatekeeper on macOS ensures that properly signed and authentic apps and other executable files, including dylibs and kexts, are executed on your Mac.
But if you want to execute an open-source tool installed by [brew](https://brew.sh) or some other way on your machine, you will usually see something like this confirmation dialog. In this case, for an app **FSNotes** installed with brew.

{{< img src="gatekeeperConfirmation.png" title="macOS Gatekeeper Confirmation Dialog" alt="macOS Gatekeeper Confirmation Dialog" full="true">}}

It's required to confirm this dialog before the app is launched.
Okay, that's fine so far.

## Adding more executable files at once to the system policy rule database

Having one executable to confirm might be fine and not a big deal. In my case, I was using a tool [OCLint](https://oclint.org/) that uses rules to lint Objective-C code. Those rules come in the form of dylibs. The current OCLint version installed on my machine has **76**! separate dylibs loaded dynamically when OCLint needs the specific rule to lint the source code.

Using OCLint for the first will ask you to load one of the rule dylibs. Accept and try again. Now the next dylibs need your confirmation, and so on. That is tedious to add all required dylibs manually. There must be a better way to solve this problem.

## The Command-Line to the Rescue

After some searching, I found out that `spctl` (System Policy Control) is the tool to modify Gatekeeper (the end-user friendly name) and manipulate the policy system rule database that decides which code is allowed to be executed and which code is not.

To find out more about `spctl` run `man spctl` in a terminal app of your choice.

Only a small subset of `spclt` options are required to solve my problem.
One thing that comes in handy is that you can create a label to add rules to this label and to enable/disable all rules that have this label.

In the end, I needed two things

### I added every OCLint rule dylib to the label OCLint

{{< highlight bash "title=I added every OCLint rule dylib to the label OCLint" >}}
find /usr/local/Caskroom/oclint/21.10/oclint-21.10/lib/oclint -name "*.dylib" -print0 | xargs -0 sudo spctl --add --label "OCLint"
{{< /highlight >}}

### I enabled all rules in the OCLint label

{{< highlight bash "title=Enable all Rules with Label OCLint" >}}
sudo spctl --enable --label "OCLint"
{{< /highlight >}}

Done! Now OCLint could work without asking for confirmation for every single dylib.

## Resources

The [Post](https://www.cnet.com/tech/computing/how-to-manage-os-x-gatekeeper-from-the-command-line/) helped me to learn about `spctl`.

I'm using the term rule here for two different systems. It might be confusing at times, but `spctl` uses the term Rule for every executable in the database. OCLint consists of linting rules for Objective-C source code.

Thanks for reading
