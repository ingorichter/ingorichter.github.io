+++
title = "Day205"
categories = ["CV19WFH"]
tags = ["WFH", "Corona", "COVID19"]
date = 2020-10-07
draft = false
+++

## WFH Day 205

I'm currently working on some very tricky programming issues at work. Things are moving slowly, and there are times when I think what the hell am I doing here. Luckily, this is a temporary state and will only get worse by working on something entirely different. Right, working on the [leetcode October challenge](https://leetcode.com/explore/challenge/card/october-leetcoding-challenge) can show me that things can get worse. Last night I spent 3 hours! On a simple (in retrospect, it was a straightforward) problem. Inserting something into a BST and return the resulting BST. Perhaps it was too late, I didn't pay enough attention to the little details along the way, but I got something working on my machine, and when I pasted it into the leetcode editor, it wasn't working anymore. Great! WHY IS THIS NOT WORKING?! I got it working locally, and now this. Sigh. I didn't get the points for that day, and I went to bed slightly frustrated about the outcome. Anyway, it should be fun and entertaining, but it wasn't.

Early this morning, I looked at the problem again and tried several things to debug the issue to make it work in leetcode. And then I finally found the stupid mistake I made. So, I could fix it and throw away 60% of my solution, since the code I wrote to turn an array with numbers into a BST was unnecessary at all. Since the input from the test case looked like an array, I built some function to create a BST from that serialized BST and then insert the new number into the BST. But the test case input was already an instance of the BST, and I just needed to binary search that tree and insert the value at the correct spot.

Lesson learned:

- read the instructions carefully
- inspect the input data from the test cases
- don't do it late at night

And perhaps use a different language with a better type system (I was initially using javascript). Looking at the TypeScript scaffold for the solution made it clear to me that the input to the function is an instance of the class defined in the comment. The function parameter didn't show the type in the javascript version, and I skipped the function comment. So, an obvious User error.

Anyway, I solved the problem today much more comfortable by being more careful.
And the Oakland Athletics won the 3rd game of the postseason beating the sh** out of the Astros. Go A's!!!

BTW: If you want to know how it feels about interviewing for a software engineering position at some high profile companies, I recommend watching this analogy for when the same principles apply for doctors.

[If Doctors were interviewed like software engineers](https://www.reddit.com/r/ProgrammerHumor/comments/j67lva/if_doctors_were_interviewed_like_software)

Mahalo 🌸
