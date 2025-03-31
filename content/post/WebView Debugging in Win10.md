+++
date = "2016-11-15T23:15:51-07:00"
draft = true
title = "WebView Debugging on Windows 10"
tags  = [ "TIL", "Tips", "Programming", "JavaScript", "WebView", "Windows10" ]
topics = [ "TIL", "Tips", "Programming", "Windows10" ]
+++
# WebView Debugging on Windows 10

I'm currently working on a new Windows 10 UWP application. Parts of this application use an embedded WebView to host a single page application (SPA). The SPA is written in Reactjs and communicates with the host application. How this communication part is realized will be discussed in another blog post.
The SPA is already in use with the OSX version of the product. The challenging part with an application running in an embedded WebView, is the lack of debugging options. There is a way make this happen on OSX, but I haven't worked on a solution for Windows. Since I have an issue with the SPA, and there are exceptions during Runtime, I need to debug the SPA in the context of the host app. As I said in the beginning, there are functions in the SPA that will call into the native host app.

Let's get started

[source, javascript]
----

<Toggle>
 <Comp1>
 <Comp2>
</Toggle>
----

The `render` method of `Toggle` looked like this
[source, javascript]
----

render() {
 const content = React.Children.count(this.props.children) > 0 ? this.props.children[0] : this.props.children[1];

 return (
  ${content}
 );

}
----

Unfortunately, this didn't work (index out of bounds), when I passed only one component instead of two.
This doesn't make sense, since the `Toggle` is supposed to toggle between two components. So, you could argue, that I broke the contract by not passing two child components to `Toggle`. That is all true.

What I want to show instead, is the fact that if you pass only one child component, then `this.props.children` is not an array anymore. `this.props.children` is the one component. Which explains the index out of bounds error.

Some information about dealing with `this.props.children` is available <https://facebook.github.io/react/docs/top-level-api.html[here>].

Thanks for reading!
