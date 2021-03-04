---
title: "Enable Flash Player Plugin in Vivaldi"
date: 2020-09-29
draft: true
categories: ["TIL", "Tips"]
tags: ["Vivaldi", "Chrome", "Browser", "Policy", "Policies", "macos"]
---

# Make Flash Flayer Plugin Work Again In Vivaldi

This is a reminder for myself to save some precious lifetime if I ever have to go through this exercise again.

I needed access to some company internal services that were only available through a website that uses a Flash UI to provide the input to the service. I never had to use this internal service before and I was surprised how much time I had to invest to get it working for that little task I had to perform.
Safari and Firefox didn't even show the Flash content or a placeholder where the content was supposed to be. They didn't offer me an option enable the Flash Plugin. I banned the Flash Player/Plugin a long time ago. This is highly insecure and outdated technology that is retired for a reason. So, why should I bother with a security risk at all. Sigh...
Would Chrome work better? I don't know?! That's the reason I'm using Vivaldi which is based on Chromium.

## TL;DR

Enable Flash Player Plugin support in [Vivaldi](https://vivaldi.com) 3.3 is discouraging to say the least. You need to configure a specific policy that will allow the Flash Player Plugin to work in content from whitelisted domain(s).
You need to provide the exact domain(s). No wildcard matching is allowed anymore.

## Enable The Flash Player Plugin

Let's walk through the steps to enable the Plugin.
Note: I show how to do it on macosx. The instructions for Windows and Linux are similar.

### Adding the Policy

Before making any changes to the Vivaldi preference file ensure that Vivaldi is not running anymore. Otherwise your changes might be overwritten.

- Open a terminal
- run `ls -al ~/Library/Preferences/com.vivaldi.Vivaldi.plist` to see if the file exist. If you ran Vivaldi before, this file should already be there. Otherwise it'll be created.

There are at least three ways to edit that preferences file

1) open it in XCode
2) convert it into plaintext xml and use your favorite editor with `plutil -convert xml1 com.vivaldi.Vivaldi`
3) use the `defaults` tool to apply the changes

I'm using #3 for this exercise.

You an use `defaults read com.vivaldi.Vivaldi PluginsAllowedForUrls` to check any existing values. There is a good chance that you won't see anything, if you never modifified that setting before. ;-)

Now we are going to run `defaults write com.vivaldi.Vivaldi PluginsAllowedForUrls -array-add "whatever.domain.com"`. This will write the value into the preferences file and you can be sure that it's properly formatted and valid.

Running this should yield that output
{{< highlight bash "title=read defaults">}}
~/%> defaults read vom.vivaldi.Vivaldi PluginsAllowedForUrls

(
    "whatever.domain.com"
)
{{< /highlight >}}

Well Done! Now you can launch Vivaldi and the Flash Player Plugin will work for that specific domain. And only that domain.

#### You Need more Domains

Okay, to add more domains to the existing ones, you can run the same command as above and add more domains as needed.

It seems that the security for the Flash Player Plugin has been very strict. One specific issue that I ran into was that wildcard domains a la `*.mydomain.com` are no longer supported. Vivaldi didn't want to accept that value when I put it in the preferences file.

And another thing that I noticed is that the Flash Player Plugin setting in Vivaldi doesn't stick. Everytime I changes this setting and closed the dialog, the setting wasn't saved. That's confusing. Rest assured that the Flash Player Plugin works without that setting.

## Check If Vivaldi Recognized the Policy

Open a new browser tab and type `vivaldi://policy` in the address bar

You should see something like this

{{< imgproc vivaldipolicy.png Resize "2400x" >}}Vivaldi Policy
{{< fancybox path="." file="vivaldipolicy.png" caption="caption" gallery="gallery" >}}


## Resources

- https://support.google.com/chrome/a/answer/187948?hl=en
- https://www.chromium.org/administrators/policy-list-3#PluginsAllowedForUrls
- https://cloud.google.com/docs/chrome-enterprise/policies/?policy=PluginsAllowedForUrls
- https://stackoverflow.com/questions/38206916/mandatory-chrome-policies-on-mac
- https://github.com/timsutton/mcxToProfile
