+++
categories = ["life"]
date = "2026-08-29T22:50:47-07:00"
description = "A simple app to practice 4-7-8 breathing"
draft = true
id = "e51ef8b6fd7e9a77900515b71420979bc596c2ae"
link = ""
tags = ["life"]
title = "Breathing App"
[params]
[[headerimage]]
  src = "header.svg"
  alt = "4-7-8 breathing: inhale for 4, hold for 7, exhale for 8"
  stretch = "cover"
+++

<!--more-->

I tell people all the time: when something is cheap and low-risk, just try it. And yet, when "breathing exercises" showed up in my research, I almost scrolled past.

Context: in August 2024 a pulmonary embolism made breathing harder and wiped out my fitness. Months later I started climbing back on the bike to rebuild my endurance. I made progress — but something was still missing. My HRV (Heart Rate Variability) still averaged around 30ms, and my sleep stayed shallow. That's where breathing exercises entered the picture. Every source I read — videos, blog posts, papers — pointed at the same low-effort fix: a low HRV feeds poor sleep and stalled recovery, and slow, deliberate breathing is one of the cheapest ways to push back. 4-7-8, a few minutes a day.

Sigh. Time to take my own advice.

## Breathing App

I found a lot of apps on the internet and in app stores that help with breathing exercises. Some of them provide guided breathing exercises for 4-7-8, alternate nostril breathing, humming bee breathing, and lion's breath, just to name a few. There are many more techniques that you can choose from.

Since I only wanted a simple app to practice 4-7-8 breathing, I didn't find one that I liked. To challenge myself, I decided to develop my own app that does one thing well.

My goals were:

- A web app
- Self-explanatory
- Web technology where possible (Web Audio, Haptics)
- Offline support (Web Worker)
- Configurable session length (1-60 mins)
- Different audio guidance
- Color themes
- Self-hosted
- No account needed!
- Data saved locally on device
- 35-day session display and streak counter

## Tech Stack

I created a React app with Vite. It seems to be a modern stack, and the out-of-the-box experience is really good IMHO. Since my day job lets me work with React on a much larger codebase, I thought it would be a breath of fresh air to use a modern incarnation of React and modern tooling.

I'm not a web designer, but I needed something that doesn't look like engineer-driven UI design. For this reason, I used my local LLM to help me with an appealing UI. I asked for a mobile-first experience, with a unique SVG icon, a nice animation for the breathing exercise, and different color themes. I like the result. It required some fine-tuning, but overall it was a great help to have a dedicated helper for the UI design. My day job lets me work with great UX designers who provide us engineers with great designs that we have to realize. For me, as a one-man show, I needed that help too, but only with access to a local LLM.

The app is designed as a single-page app (SPA). The user can navigate between three pages:

- the Home page, which starts a session
- the Setup page, for duration, audio guidance, and color theme
- the Stats page, with the 35-day history and streak counter

{{< img src="screenshot-home.png" alt="Home page: the 4-7-8 wordmark, a streak and session count, and a Begin button" caption="Home — start a session" lightbox="true" showMeta="false" width="300px" >}}

{{< img src="screenshot-setup.png" alt="Setup page: a duration slider from 1 to 60 minutes and audio guidance options" caption="Setup — session length, audio, and theme" lightbox="true" showMeta="false" width="300px" >}}

{{< img src="screenshot-stats.png" alt="Stats page: streak, session, and minute totals above a 35-day grid" caption="Stats — history and streak" lightbox="true" showMeta="false" width="300px" >}}

The only feature I couldn't realize with web technologies was haptic feedback. It can't be triggered reliably from a web app.

## Availability

The app is available at [breathing.ingo-richter.io](https://breathing.ingo-richter.io), or via the __Breathing__ entry in the top navigation of this site. Open it and you can start right away and try it out.

Let me know what you think. Is this helpful for you? Is there anything missing? Feedback welcome in the comments below.

Mahalo 🌸
