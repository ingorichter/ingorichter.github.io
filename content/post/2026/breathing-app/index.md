+++
categories = ["life"]
date = "2026-05-01T22:50:47-07:00"
description = "A simple app to practice 4-7-8 breathing"
draft = true
id = "e51ef8b6fd7e9a77900515b71420979bc596c2ae"
link = ""
tags = ["life"]
title = "Breathing App"
+++

<!--more-->

I want to improve my endurance after being hit by a medical issue. Another goal is to improve my sleep quality and reduce stress. I did some research and found videos, blog posts, and other publications where different people mentioned that a low HRV (Heart Rate Variability) could be contributing to poor sleep and a lack of progress on endurance despite regular exercise. One way to improve sleep and endurance could be breathing exercises. They are generally recommended for stress reduction.

## Breathing App

I found a lot of apps on the internet and in app stores that help with breathing exercises. Some of them provide guided breathing exercises for 4-7-8, alternate nostril breathing, humming bee breathing, Lion's breath, just to name a few. There are many more techniques that you can choose from.

Since I only wanted a simple app to practice 4-7-8 breathing, I didn't find one that I liked. To challenge myself, I decided to develop my own app that does one thing well.
My goals were to

- Develop a web app
- Self-explanatory
- Use web technology where possible (Web Audio, Haptics)
- Offline support (Web Worker)
- Configurable session length (1-60 mins)
- Different audio guidance
- Color themes
- Self hosted
- No account needed
- Save data locally on device
- 35-day session display and streak counter

## Tech Stack

I created a React app with Vite. It seems to be a modern stack, and the out-of-the-box experience is really good IMHO. Since my day job lets me work with React on a much larger codebase, I thought it would be a breath of fresh air to use a modern incarnation of React and modern tooling.

I'm not a web designer, but I needed something that doesn't look like engineer-driven UI design. For this reason, I used my local LLM to help me with an appealing UI. I asked for a mobile-first experience, with a unique SVG icon, a nice animation for the breathing exercise, and different color themes. I like the result. It required some fine-tuning, but overall it was a great help to have a dedicated helper for the UI design. My day job lets me work with great UX designers who provide us engineers with great designs that we have to realize. For me, as a one-man show, I needed that help too, but only with access to a local LLM.

The app is designed as a single-page app (SPA). The user can navigate between 3 different pages:

- the Home page
- the Setup page
- the Stats page

## Hosting

The app is available on this blog. You can find it by clicking the menu entry **Breathing** in the top navigation of this site.
This will open the app, and you can start right away and try it out.
