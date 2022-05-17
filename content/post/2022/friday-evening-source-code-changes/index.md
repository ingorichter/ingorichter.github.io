+++
title = "Friday Evening Source Code Changes"
categories = ["TTA", "TIL"]
tags = ["Coding", "Sleepiness", "TIL"]
date = 2022-05-16
draft = false
+++

## Well, Crap, what a waste of time

One would guess that I should have known better with the work experience I accumulated in the software engineering field.

But, it's Friday evening, after our social team meeting, and I am still excited to finish something substantial for this feature that I'm working. Lots of moving parts, refactored code, loose ends, and hastily glued together code without any safety net. A couple of new unit tests for the new feature and some legacy code that I have to touch. Very picky and sensible legacy code. I'm careful not to break any existing and battlefield-proven code that is used by ~25M monthly active users across multiple products. Run the existing unit tests between more considerable changes and ensure that it stays in the green.

And then, I discovered a potential piece of new code that could be expressed in a more concise, clearer, and compact way by leveraging some framework class that should help avoid duplication—quickly refactoring and changing the new code. There is no unit test available yet, and highly confident of hitting a home run with these last changes for the week. Everything looks good. I prepare the commit and send it off into the weekend. It's nearly 10 PM—time to stop for now.

Monday morning comes, and after some early meetings, I look at my notes from last Friday. Things I wanted to do and things I wanted to refine. Launch the test app and use the new feature. But wait, something is off. I'm getting errors from the API endpoint that wasn't there last Friday when I left everything behind.

Well, it's a staging environment. Something must have been updated something recently. My co-workers for that endpoint live in a different Geo. Everything is possible, but I'm still annoyed that I can't take the feature for a test ride. Sigh... I inspect the output from the API, and it's an error I haven't seen before. Hm, what's that? That doesn't look like the errors usually come from that endpoint. Something is off. Let me check with our development branch real quick and see how the endpoint behaves. 

Strange, everything seems to be okay. That's weird; why does my working branch trigger that strange error? I didn't change anything between Friday and now... Wait a minute. Let me look at my last commit from Friday night. Hm, nothing suspicious. That's weird. What the hell is going on? I can make the request, and it comes back with an error? What did I change? Hmm, I used the framework class to make everything more concise, clearer, and compact. Right, I remember now. That great optimization late Friday night. That saved a couple of lines and seemed to have broken something, which should make everything better.

Well, I have to admit that I missed that class and broke something that impacted the generated URL to call the endpoint. Something was missing in the generated URL that triggered that never before seen error. After reading the docs for that class, I could quickly fix that issue. But it took me nearly 45 minutes to make sense of the things I saw.

Lesson learned: Do not make simple-looking changes late Friday night! Especially when you don't run or test the code after changing it. Leave those changes for Monday or the following day. Take notes and go home.

Cheers!