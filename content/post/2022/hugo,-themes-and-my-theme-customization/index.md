+++
title = "Hugo, Themes and My Theme Customization"
categories = ["TIL"]
tags = ["TIL", "hugo", "themes", "customization"]
date = 2022-01-18
draft = false
+++

## TL;DR

[Hugo](https://gohugo.io)'s file lookup magic was biting me and was causing the 3rd party template to use a file with the same name from my blog assets directory.

## How to waste lots of hours

I use [Hugo](https://gohugo.io) for my [Blog](https://ingo-richter.io) with a custom theme [hugo future imperfect slim](https://github.com/pacollins/hugo-future-imperfect-slim).

I made some customizations to my blog a while ago. I added [baguetteBox.js](https://feimosi.github.io/baguetteBox.js/) for better image galleries and [lazySizes](https://afarkas.github.io/lazysizes/index.html) to better support different image sizes in the gallery. I [bundled the files](https://gohugo.io/hugo-pipes/bundling/) and minified them in a single javascript file to reduce the number of requests to the server.

I combined the mentioned JavaScript files into one file by having a customized version of `scripts.html` file that I copied from the original template source into the `layouts/partials` directory. The following lines show the steps to combine the js files into `js/scripts.js`.

{{< highlight bash >}}
{{ $baguetteBox := resources.Get "js/external/baguetteBox.js" }}
{{ $lazysizes := resources.Get "js/external/lazysizes.js" }}
{{ $main := resources.Get "js/main.js" }}
{{ $scripts := slice $baguetteBox $lazysizes $main | resources.Concat "js/scripts.js" | resources.Minify }}
<script src="{{ $scripts.RelPermalink }}"></script>
{{< /highlight >}}

The problematic file in this process is `js/main.js`. The theme uses a file with this name as a template to generate other files during the blog creation. The template mechanism was using my version of the file, and the template mechanism failed, and then some essential files from the theme were missing. Those missing generated files led my blog to **misbehave** in some areas where the JavaScript files were required (search, language selection, sharing).

The [Lookup Order](https://gohugo.io/templates/lookup-order/) describes how the lookup works to create the final layout for a section. What they don't mention at all is the fact that the lookup logic is not only applied to layout files but also JavaScript files. I don't know if this holds for other file types.

After some frustrating hours of debugging and examining my blog configuration, and inspecting the theme directory structure, I finally resolved this issue. I renamed my file from `main.js` to `externMain.js`. Any name would be better than `main.js`.

So, if you are encountering broken functionality or missing files after tinkering with a Hugo theme, I recommend inspecting your modified and added files. Perhaps you have a similar situation that I was fighting.

Thanks for reading!
