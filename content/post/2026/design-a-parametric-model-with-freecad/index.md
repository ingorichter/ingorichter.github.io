+++
categories = ["TIL"]
date = "2026-01-26T23:07:27-08:00"
description = ""
draft = true
id = "73f355f8ead362a2b56281f80c6185b6d8b94f7b"
link = ""
tags = ["TIL"]
title = "Design a Parametric Model with FreeCad"
+++

<!--more-->

## Tl;DR

I'll design a parametric model with FreeCad, an open source CAD program, to allow for easy customization. I needed to box or tray with small compartments to store a handful of little glass bottles. I wanted something that makes it easier for me to store the bottles conveniently either in the cabinet or the fridge.

## Initial Design

I started by sketching out the design on my Remarkable tablet. I decided on a rectangular box with a grid of compartments. Each compartment would be sized to fit one glass bottle snugly. I didn't want to have a lid, since this would have made the box much bigger. It should have a height tall enough to keep those bottles safe. But since this is a parametric model, I will be able to easily adjust the height without having to redesign anything.

![Initial Sketch](initial_sketch.png)

## FreeCAD Modeling

Let's open FreeCad and create a new Project.
1. **Create a New Sketch**: Start by creating a new sketch on the XY plane. Draw a rectangle that represents the base of the box. Use the dimension tool to set the length and width according to your design.
