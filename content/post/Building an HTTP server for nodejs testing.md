+++
date = "2016-06-21T21:15:51-07:00"
draft = true
title = "Building an HTTP server for nodejs testing"
tags  = [ "Testing", "Tips", "Programming", "nodejs"]
topics = [ "Tips", "Programming" ]
+++

## The Situation

The are situations, where you create a piece of software, that downloads somethings from the internet. It can be something like an RSS feed, some JSON from any API or some arbitrary data (this is my case). Whatever it is, writing tests for your code will be a bit more work, when you want to be able to

- be independent of that API endpoint for testing
- run and develop offline

## What can you do about it?

There are a couple of possible solutions to that situation. You could either mock the communication with the API endpoint, by using mock objects that deliver the right mocking data to the caller. Or you can spin up your own server during test runs and deliver the content to the caller. Since the first solution is well proven, I have chosen the second one to use in one of my projects, since I wanted to learn something new.

I will show you, how to write a reusable http server to serve whatever content you need to make your tests happy.

## Let's get started

INFO: Make sure that you have nodejs (4.4.x) and npm (2.15.x) installed. Anything newer might work, but that is my configuration.