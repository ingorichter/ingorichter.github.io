+++
author = "Ingo Richter"
date = "2017-04-06T11:55:51-07:00"
categories = ["Git","Programming"]
tags = ["Git", "Programming", "Tips", "Tricks", "Tools", "TIL"]
title = "Efficient JavaScript Unit Testing with Jest and Snapshots"
description = "Make your software testing life easier with Jest and Snapshots to test your javascript code"
draft = false
+++

Let's start with a bold statement:

> **We all love to write unit great tests for our code. More or less.**
>
> — Unknown Programmer

Writing unit tests for my code mostly follows this pattern

1. Write a test and make it fail (red)
2. Write the function to fix the test (implement function)
3. Start over with step 1

For one of my projects, I was using [jest](https://facebook.github.io/jest/). It's fast now, and it has several features that I highly value. Most of them integrated code coverage and Snapshot testing.

# Snapshot testing? What's that?

When I first saw the part about Snapshot testing, I wasn't interested. Okay, it was more that I thought, well, I don't see a big advantage here over the traditional approach of testing my code. I'm calling functions and make sure that the result of those functions matches my expectations. That's pretty simple with a function that returns a simple result
Writing unit tests for my code mostly follows this pattern

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
function add(a, b) {
  return a + b;
};

test("Verify that 1 + 3 equals 4", () => {
  expect(add(1, 3)).toBe(4);
});
{{< /highlight >}}

This is simple and doesn’t require much work.

How about this? 

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
function createTodoItem(subject, projects, contexts, due) {
    return {
        "subject": subject,
        "projects": projects,
        "contexts": contexts,
        "due": due,
        "completed": false,
        "archived": false,
        "isPriority": false
    }
};

test("Verify that new todo item has all required fields", () => {
    const newTodoItem = createTodoItem("New Task", ["blog"], ["learn", "programming"], "2017-04-17");
    const expectedTodoItem = {}

    expect(newTodoItem).toEqual(expectedTodoItem);
});
{{< /highlight >}}

As expected, the output is telling me, that there is something missing. Yes, I didn’t write yet the expected object to compare the result with. I’m too lazy, and I always want to avoid writing it. What I’m doing instead, is to call the function, copy the result and create my expected result object with this data. But for now, I’m not going to do it. Let’s see, how Snapshot testing will help solve this task.

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
Verify that new todo item has all required fields

    expect(received).toEqual(expected)

    Expected value to equal:
      {}
    Received:
      {"archived": false, "completed": false, "contexts": ["learn", "programming"], "due": "2017-04-17", "isPriority": false, "projects": ["blog"], "subject": "New Task"}

    Difference:

    - Expected
    + Received

    -Object {}
    +Object {
    +  "archived": false,
    +  "completed": false,
    +  "contexts": Array [
    +    "learn",
    +    "programming",
    +  ],
    +  "due": "2017-04-17",
    +  "isPriority": false,
    +  "projects": Array [
    +    "blog",
    +  ],
    +  "subject": "New Task",
    +}

      at Object.<anonymous>.test (__tests__/newTask-test.js:7:25)
      at process._tickCallback (internal/process/next_tick.js:109:7)

 PASS  __tests__/add-test.js

Test Suites: 1 failed, 1 passed, 2 total
Tests:       1 failed, 1 passed, 2 total
Snapshots:   0 total
Time:        1.042s
Ran all test suites.
{{< /highlight >}}

Yeah, I was lazy and didn’t populate `expectedTodoItem` with all the fields I was expecting. This is the point, where Snapshot testing comes into play. It helps me lazy programmer to avoid writing unnecessary code only to verify my assumptions about the outcome of that function.

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
function createTodoItem(subject, projects, contexts, due) {
    return {
        "subject": subject,
        "projects": projects,
        "contexts": contexts,
        "due": due,
        "completed": false,
        "archived": false,
        "isPriority": false
    }
};

test("Verify that new todo item has all required fields", () => {
    const newTodoItem = createTodoItem("New Task", ["blog"], ["learn", "programming"], "2017-04-17");

    expect(newTodoItem).toMatchSnapshot();
});
{{< /highlight >}}

And here the result.

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
PASS  __tests__/newTask-test.js
PASS  __tests__/add-test.js

Test Suites: 2 passed, 2 total
Tests:       2 passed, 2 total
Snapshots:   1 passed, 1 total
Time:        0.816s, estimated 1s
Ran all test suites.
{{< /highlight >}}

## Three notable things

1. I still didn’t provide a full-fledged object that matches my expectation
2. `toMatchSnapshot()` was the only code change in the test
3. The number of Snapshots in the status output of Jest is now 1!

What happened? Jest was taking a Snapshot for that test and was happy with the result. Under the hood, Jest created a `__snapshots__` directory in my `__tests__` directory and saved the output of the test result. The file is named after the file containing the test. In this case, it’s `newTask-test.js.snap`. Here are the contents of that Snapshot file.

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
// Jest Snapshot v1, https://goo.gl/fbAQLP

exports[`Verify that new todo item has all required fields 1`] = `
Object {
  "archived": false,
  "completed": false,
  "contexts": Array [
    "learn",
    "programming",
  ],
  "due": "2017-04-17",
  "isPriority": false,
  "projects": Array [
    "blog",
  ],
  "subject": "New Task",
}
`;
{{< /highlight >}}

The key of the exports object is the name of the test itself. The value of it is the result from `createTodoItem("New Task", ["blog"], ["learn", "programming"], "2017-04-17")`. That is great. I didn’t have to type a line of code for the expected result of this function. By doing a quick visual inspection of the output, I can confirm that this is the expected output.

Now it gets interesting. I’m going to change the return object of the function. The result object will have a new key `completedDate` and the `completed` flag will be removed. Let’s see how Jest handles the situation without making any change to the existing, and currently passing, test.

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
 FAIL  __tests__/newTask-test.js
  ● Verify that new todo item has all required fields

    expect(value).toMatchSnapshot()

    Received value does not match stored snapshot 1.

    - Snapshot
    + Received

    @@ -1,8 +1,8 @@
     Object {
       "archived": false,
    -  "completed": false,
    +  "completedDate": "",
       "contexts": Array [
         "learn",
         "programming",
       ],
       "due": "2017-04-17",

      at Object.<anonymous>.test (__tests__/newTask-test.js:8:25)
      at process._tickCallback (internal/process/next_tick.js:109:7)

 PASS  __tests__/add-test.js

Snapshot Summary
 › 1 snapshot test failed in 1 test suite. Inspect your code changes or run with `npm test -- -u` to update them.

Test Suites: 1 failed, 1 passed, 2 total
Tests:       1 failed, 1 passed, 2 total
Snapshots:   1 failed, 1 total
Time:        1.113s
Ran all test suites.
{{< /highlight >}}

The output of the test run informs me that the `Received value does not match stored snapshot 1`. That is correct, and it was expected. But more importantly, Jest tells me to inspect my code changes or run the tests again with a specific flag to update the snapshot. Since it was an intentional change, I’m going to run the test again with `npm test -- -u` to update the Snapshot.

{{< highlight javascript "linenos=inline,linenostart=1,title=test.js">}}
> jest "-u"

 PASS  __tests__/newTask-test.js
 PASS  __tests__/add-test.js

Snapshot Summary
 › 1 snapshot updated in 1 test suite.

Test Suites: 2 passed, 2 total
Tests:       2 passed, 2 total
Snapshots:   1 updated, 1 total
Time:        1.115s
Ran all test suites.
{{< /highlight >}}

The Snapshot got updated and reflects the current implementation of my function. Well done! No code is written to create the expected result object. This is where Snapshot testing is awesome.

## Summary

I hope that this example helped to understand the Snapshot testing capability of Jest. IMHO, this approach is excellent for two reasons:

1. I don't have to write code to compare complex result objects
2. Less test code to write, easier to read, more time to work on features

Snapshot testing might not be necessary/wanted for all kind of tests. You might choose the traditional way for simpler functions. To verify complex result objects, this is an efficient way for testing. Having to write less code is always a great way to improve efficiency.

Don't hesitate to contact me, if you have questions or suggestions. You can leave a comment below or find me on the social networks mentioned at the top of this post.

**Thank you very much for reading!**
