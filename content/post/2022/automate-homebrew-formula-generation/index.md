+++
title = "Automate Homebrew Formula Generation"
categories = ["TIL"]
tags = ["TIL"]
date = 2022-10-21
draft = true
+++

## TL;DR

Things I learnt while automating the update and release of a Homebrew cask with github workflows.

## Testing

## Workflows and their specialities

- manual vs. automatic triggering
- preserve information between steps
- replace vs. recreation (use sed to replace values in the existing Formula or recreate it entirely)
