+++
date = "2016-08-15T23:15:51-07:00"
draft = false
title = "TIL - Reactjs optimization that cost me some time"
tags  = [ "TIL", "Tips", "Programming", "JavaScript", "Reactjs" ]
topics = [ "TIL", "Tips", "Programming" ]
categories = [ "TIL", "Tips", "Programming" ]
+++

I was building a Reactjs component, that should toggle between two child components.

{{< highlight jsx session"linenos=inline,hl_lines=2 3">}}
<Toggle>
 <Comp1>
 <Comp2>
</Toggle>
{{< /highlight >}}

The `render` method of `Toggle` looked like this
{{< highlight javascript session"linenos=inline,hl_lines=2 3">}}
render() {
 const content = React.Children.count(this.props.children) > 0 ? this.props.children[0] : this.props.children[1];

 return (
  ${content}
 );
}
{{< /highlight >}}

Unfortunately, this didn't work (index out of bounds), when I passed only one component instead of two.
This doesn't make sense since the `Toggle` is supposed to toggle between two components. So, you could argue, that I broke the contract by not passing two child components to `Toggle`. That is all true.

What I want to show instead, is the fact that if you pass only one child component, then `this.props.children` is not an array anymore. `this.props.children` is the one component. Which explains the index out of bounds error.

Some information about dealing with `this.props.children` is available [here](https://facebook.github.io/react/docs/top-level-api.html).

Thanks for reading!
