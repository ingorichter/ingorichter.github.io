+++
title = "Dayjs Extension Usage"
categories = ["TIL", "javascript", "typescript"]
tags = ["TIL"]
date = 2023-02-14
draft = false
+++

## Enable extensions for dayjs

I was working on a [small project](https://github.com/ingorichter/Biorhythm) to sharpen my Javascript and Typescript skills. Nothing fancy.

The project deals with data calculations, and I was looking for a modern replacement of momentjs. I found [dayjs](https://day.js.org/en/), which seemed to be a suitable replacement.

As I mentioned, I had to find the number of days between the two dates. The documentation of dayjs mentioned a method to calculate the difference between two dates as duration. The duration could then be represented as days. That is exactly what I needed for my calculations.

I somehow missed that I had to `import duration from 'dayjs/plugin/duration';`. But that still didn't work. `duration` was still undefined.
I missed a crucial part in the documentation (perhaps I was too tired or impatient), but the most crucial part to add those additional methods to dayjs is to call `dayjs.extend(duration);`. This call to `extend` will make the methods and properties available on the dayjs object.

Lesson learnt: RTFM! Next time I will do better 🤞🏼