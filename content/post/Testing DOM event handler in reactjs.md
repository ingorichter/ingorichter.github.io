---
title: "Testing raw DOM Event Handler in Reactjs"
date: 2018-08-12T16:38:57-07:00
draft: false
categories: ["Tips"]
tags: ["Reactjs", "Programming", "Testing", "DontForget"]
---

This is a reminder to myself. And to anybody who needs a creative solution to test an event handler directly attached to a DOM node of a react component.

Last Friday I ran into the situation to test my react component to ensure that the state updates correctly when the `pointerenter` and `pointerleave` event fires.
Testing for these events is usually no big deal when you use reactjs in one way or the other (either web or native). At work we use an internal framework that is react API compatible and implements most of the features of react. Most of them, but not all.

I ran into the situation where I have the `pointerenter` event handler defined, but they didn't fire. The team recommended to replace it with an event handler directly attached to the DOM node by

* assign a ref to the component
* attach the event handler to the ref

This is how it looked like
{{< highlight jsx >}}
class ImageHover extends React.Component {
	constructor(props) {
		super(props);
		
		this._hoverBoxRef = React.CreateRef();
	}

	function _toggleHoverState = (state) => {
		this.setState({ isNormal: state });

    function componentDidMount() {
        this._hoverBoxRef.current.addEventListener('pointerenter', () => this._toggleHoverState(false));
        this._hoverBoxRef.current.addEventListener('pointerleave', () => this._toggleHoverState(true));
    }

    function componentWillUnmount() {
        this._hoverBoxRef.current.removeEventListener('pointerenter', () => this._toggleHoverState(false));
        this._hoverBoxRef.current.removeEventListener('pointerleave', () => this._toggleHoverState(true));
    }

	render () {
		style = this.state.isNormal ? "normal" : "hover";
		return (
			<div
				className={ style }
				onClick={this.props.onClick}
				ref={this._hoverBoxRef}
            />
		);
	}
{{< / highlight >}}

To ensure that the component changes the style to `hover` when the `pointerenter` event fires and back to `normal` when `pointerleave` is fired can usually achieved by using the rendered component and call `.simulate("pointerEnter")` when using jest and enzyme.

Normal test

{{< highlight jsx >}}
cb = jest.fn();
imageHover = mount(<ImageHover imageName={"phone"} onClick={cb} />);
	
it("should change state on pointerEnter", () => {
	imageHover.simulate("pointerEnter");
    expect(imageHover.state().isNormal).toEqual(false);
});
{{< / highlight >}}

Since the `pointerEnter` event didn't fire in my situation, I had to find another way to trigger that event. Here is the modified test

{{< highlight jsx >}}
cb = jest.fn();
imageHover = mount(<ImageHover imageName={"phone"} onClick={cb} />);

it("should change state on pointerEnter", () => {
	const domNode = imageHover.getDOMNode();
	const event = new Event("pointerenter");
	domNode.dispatchEvent(event);
	expect(imageHover.state().isNormal).toEqual(false);
});
{{< / highlight >}}

The tiny difference is getting access to the underlying DOM element during the test execution and dispatch the `pointerenter` event on that DOM node.
I've omitted the event details in this example since they aren't relevant for the demo purpose. Perhaps there is an alternative solution to achieve the same result without the direct DOM access. Let me know, and I'm happy to update my test code.

**Thank you very much for reading!**
