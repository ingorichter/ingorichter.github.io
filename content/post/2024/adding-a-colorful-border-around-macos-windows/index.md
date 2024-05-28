+++
categories = ["TIL"]
date = "2024-05-27T10:23:58-07:00"
description = "I found this little tool that allows to add a colorful border for macOS Windows"
draft = true
id = "25edb447bdef493cca125917369763e196184c78"
link = ""
tags = ["TIL", "macos", "tools"]
title = "Adding a Colorful Border Around macOS app Windows"
+++
[1]: https://github.com/FelixKratz/JankyBorders "JankyBorders"


<!--more-->

## TL;DR

[JankyBorders][1] is a tool that allows you to add a colored border around macOS app windows. This is helpful, especially in dark mode, to better see the window border and identify which application window is in front and active.

With a simple configuration file, it’s possible to specify the colors for the active and inactive windows. The program has more customizable options than I will discuss here. I focus on defining the colors for the active window and the inactive windows. I will also show how to use gradients and glow for borders.

## Installation

The easist way is to use homebrew. The instructions are available from [JankyBorders][1]. I mention the steps here to save you from opening another website. Open a new terminal window of your choice and type the following

{{< highlight bash >}}
brew tap FelixKratz/formulae
brew install borders
{{< /highlight >}}

After installation, type **borders &** and after pressing enter, and a possible small delay, you will see a border around all the open application windows. You will see a white border around your terminal window.

{{< img src="finder-window-with-white-border.png" title="Finder Windows with White Border" alt="Finder Windows with White Border" full="true" round="0">}}

> The border might not be easy to see in light mode. I switched to dark mode for demo purposes.

It's important to leave the borders program running. Therefore, I appended it with the **&** to ensure that the process is running in the background. To avoid having to launch borders everytime you restart your machine, you can create a **LaunchAgent** config and ensure that the program is launched automatically and runs in the background. If you installed borders with homebrew, you will automatically have a LaunchAgent config installed alongside the program.

You can enable borders as LauchAgent by running the following command

{{< highlight bash >}}
brew services start borders
{{< /highlight >}}

You can disable it by running the following command

{{< highlight bash >}}
brew services stop borders
{{< /highlight >}}

## Configuration

> After each change in the config file, you need to restart the `borders` program to apply the changes.

### Colors for active and inactive windows

Although there is a way to provide the config on the command line whan launching borders, I recommend to create a config file in the **$HOME/.config/borders** directory. The config file should be named **borderrc**. Technically, it's a shell script that will launch borders with the provided options.

By default, all the colors are solid. But we can change them to be gradients or glow. Very nice feature.

Color values are defined in the form of **0xAARRGGBB**.

| Option | Description |
| --- | --- |
| **AA** | The Alpha value controls the opacity. 0 is fully transparent and 255 is fully opaque. |
| **RR** | The Red value |
| **GG** | The Green value |
| **BB** | The Blue value |

All values are in hex and range from 00 to FF. It doesn't matter if they are in lower or upper case.

The config file should look like this

> I have a Retina display on my macbook and use the hidpi option.

{{< highlight bash >}}
#!/bin/bash

options=(
    hidpi=on
    active_color=0xff0000FF
)

borders "${options[@]}"
{{< /highlight >}}

I changed the active border color to blue (RGB 0000FF).
{{< img src="finder-window-with-blue-border.png" title="Finder Windows with Blue Border" alt="Finder Windows with Blue Border" full="true" round="0">}}

Inactive windows can have a different border color assigned. Let's change the default color to for inactive windows to red (RGB FF0000).

{{< highlight bash >}}
#!/bin/bash

options=(
    hidpi=on
    active_color=0xff0000FF
    inactive_color=0xffFF0000
)

borders "${options[@]}"
{{< /highlight >}}

{{< img src="finder-windows-with-active-and-inactive-border.png" title="Finder Windows with active and inactive boder color" alt="Finder Windows with active and inactive border color" full="true" round="0">}}

### Gradients

You can also use gradients to provide a color gradient for the border. The value for any color can be a gradient in the form of gradient(top_left=0xffFF0000,bottom_right=0xff00FF00) or gradient(top_right=0xffFF0000,bottom_left=0xff00FF00).
> It's important to have the exact format of the gradient definition, otherwise the border will not be rendered. I'm using zsh and the gradient definition has be quoted.

The config file should look like this. I increased the border width to 20 to better see the gradient

{{< highlight bash >}}
#!/bin/bash

options=(
    hidpi=on
    width=20.0
    active_color="gradient(top_left=0xffFF0000,bottom_right=0xff00FF00)"
)

borders "${options[@]}"
{{< /highlight >}}

{{< img src="finder-window-gradient-border.png" title="Finder Window with gradient from red to green" alt="Finder Window with gradient from red to green" full="true" round="0">}}

### Glow

You can also use a glow effect for the border. Any color can be used to defione a glow effect in the form of glow(0xffFF0000). This glow definition will provide a red glow effect to the border. It looks a bit like a neon light around the window.

The config file should look like this

{{< highlight bash >}}
#!/bin/bash

options=(
    hidpi=on
    width=20.0
    active_color="glow(0xffFF0000)"
)

borders "${options[@]}"
{{< /highlight >}}

{{< img src="finder-window-glow.png" title="Finder Window with glow effect" alt="Finder Window with glow effect" full="true" round="0">}}

## Allow and Deny border for specific applications

You can also allow and deny applications from having a border. Unfortunately, the naming of this feature is not well thought out, since it's using the blacklist and whitelist notion that should be avoided IMHO.

Specify the name(s) of the application in the blacklist and whitelist will only allow and deny the spcificly mentioned applications. All other applications will or will not have a border.

The config file should look like this

{{< highlight bash >}}
#!/bin/bash

options=(
    hidpi=on
    width=20.0
    active_color=0xff0000FF
    blacklist="Finder"
    whitelist="Safari"
)

borders "${options[@]}"
{{< /highlight >}}

{{< img src="window-blacklist-whitelist.png" title="Safari windows are not allowed to have a border, but the Finder window is" alt="Safari windows are not allowed to have a border, but the Finder window is" full="true" round="0">}}

## Conclusion

IMHO the best way to add a border around macOS app windows is to use the **JankyBorders** program. I hope you'll find it useful too. There are more options than I mentioned here. You can read about them by running **man borders** in the terminal.

If you have any feedback, please let me know.

Thanks for reading!
