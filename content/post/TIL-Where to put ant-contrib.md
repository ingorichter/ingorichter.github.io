+++
date = "2016-06-16T20:15:51-07:00"
draft = false
title = "TIL - where to put ant-contrib"
tags  = [ "TIL", "Tips", "Programming", "Java", "Ant" ]
topics = [ "TIL", "Tips", "Programming" ]
categories = [ "Tips", "Programming" ]
+++

I was testing an [ant](https://ant.apache.org/) based build script change today. And I thought [ant](https://ant.apache.org/) was already retired. 

Running the script led to a lot of warnings about a missing library. I asked the person, if there are any dependencies for [ant-contrib](http://ant-contrib.sourceforge.net/). His response was "yes, you need to install [ant-contrib](http://ant-contrib.sourceforge.net/)".

First of all, I didn't have [ant](https://ant.apache.org/) installed. But that was easy with

{{< highlight bash >}}
irichter@irichter-MacBookPro:~ brew2 install ant
{{< /highlight >}}

Unfortunately, [ant-contrib](http://ant-contrib.sourceforge.net/) wasn't available via homebrew, so I had to download it and place it... where?
Ah, in the `lib` folder of your [ant](https://ant.apache.org/) installation. Okay, that might one solution. I remembered, that years ago I was using it in a different way. There was another location where ant was looking for additional jars.

## This worked for me 

. create or locate the `~/.ant/lib` directory
. copy all additional jars in this directory

From now on, [ant](https://ant.apache.org/) will be able to find [ant-contrib](http://ant-contrib.sourceforge.net/) and I don't have to mess around with the [ant](https://ant.apache.org/) installation directory.
Clean, nice and simple solution.

NOTE: I don't know, if this will work on Windows in the same way.

Thanks for reading!