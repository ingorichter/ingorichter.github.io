+++
title = "TIL - Adding Swift Code to Objective-C Project"
categories = ["TIL"]
tags = ["TIL", "Swift", "Objective-C"]
date = 2022-02-28
draft = false
[[images]]
  src = "post/2022/til-adding-swift-code-to-objective-c-project/NevadaFallsYosemite.jpg"
  alt = "Nevada Falls Yosemite National Park"
  stretch = "horizontal"
+++

## TL;DR

Adding Swift Code to Objective-C Project

1) Ensure your Swift class derives direct or indirect from NSObject
2) Ensure your Swift class is `public` to ensure the `YourProjectName-Swift.h` header generation
3) Prefix the class to expose it to Objective-C. Any Property or method needs its own `@objc` annotation to be visible from Objective-C.
4) Use the `@objcMembers` annotation to expose all properties and methods of the Swift class

## Reminder for myself

I learned a couple of essential things about mixing Objective-C and Swift in one project.
I was using Swift for unit tests already, and that worked fine.
Now, I wanted to implement a new class in Swift. But I wanted to use that class in an existing Objective-C class.

So far, so good. There is a lot of information on the internet about transitioning your Objective-C codebase to Swift. Everything I found looked pretty straightforward, and I wasn’t expecting a time sink by adding a simple Swift class to the project. But here we go…
I created the new Swift class `WithLoveFromSwift` with one method, `saySomethingNice`. Pretty simple as a starting point. 

{{< highlight swift >}}
class WithLoveFromSwift {
    func saySomethingNice() {
        return "Hello from Swift ❤️"
    }
}
{{</ highlight >}}

I wanted to add that Swift class to the existing Objective-C implementation in the next step. And that’s where the problems started. I read that I have to add `#import FancyGreeterApp-Swift.h` in my Objective-C file to use the new Swift class. And that file is not created by XCode so that you can easily find it. But it will be there once you start compiling. They said. But it didn’t work. The import was causing an error, and the shiny new class didn’t appear in the code completion proposals.

I spent a reasonable amount of time checking my project settings and other things I might have missed. It seemed that others had this problem too, and I wasn’t alone. But this didn’t help me resolve the issue.

After more reading and confusion, I finally saw some slightly different code that deviated from mine. Their Swift class was public! Guess what? After adding public to my Swift class and compiling, the error regarding the import statement went away. Really? Public? That’s all that was missing?

{{< highlight swift >}}
@objc public class WithLoveFromSwift {
    func saySomethingNice() {
        return "Hello from Swift ❤️"
    }
}
{{</ highlight >}}

Anyway, it was compiling, and that was the most important thing.

Now on to the next issue: my shiny class has a property `greetingLanguage`. This property should be accessible from Objective-C to set the language before creating a greeting. But the compiler once again was complaining that this property didn’t exist. Okay, I’m confused again. The property was public, in a public class. What else is needed?

{{< highlight swift >}}
@objc public class WithLoveFromSwift {
    public var greetingLanguage = "en"

    func saySomethingNice() {
        if greetingLanguage == "de" {
            return "Hallo Swift ❤️"
        } else {
            return "Hello Swift ❤️"
        }
    }
}
{{</ highlight >}}

It turns out the `@objc` annotation at the class level exposed just the Swift class. If you want to expose the properties too, or some other methods, then you either have to prefix every property with `@objc` or you can use the `@objcMembers` annotation to enable access to all properties and methods of the Swift class.

Okay, now I got it 👍🏼

{{< highlight swift >}}
@objcMembers public class WithLoveFromSwift {
    public var greetingLanguage = "en"

    func saySomethingNice() {
        if greetingLanguage == "de" {
            return "Hallo Swift ❤️"
        } else {
            return "Hello Swift ❤️"
        }
    }
}
{{</ highlight >}}

Thanks for reading