---
layout: post
title: "Two Years on Linux with AI: Emancipation or a Swapped Dependency?"
lang: en
translation: "/2026/08/03/linux-ia-autonomia-dependencia.html"
permalink: /en/2026/08/03/linux-ai-autonomy-dependency.html
category: "General"
image: /assets/images/posts/linux-ia-autonomia-dependencia.webp
---

Last week the laptop stopped waking from suspend. Black screen, fan spinning, and only `Ctrl+Alt+F3` would hand me back a terminal. I pasted the output of `journalctl -b -1 -p err` into a conversation with an AI, got two hypotheses ranked by likelihood, tested the first one, and was back at work in twenty minutes. In 2020 that same error would have eaten an entire evening of forum threads and probably ended in a reinstall.

![Isometric maze crossed by a golden thread running off the edge of the frame](/assets/images/posts/linux-ia-autonomia-dependencia.webp)

The gain is real and I use it every day. What I cannot tell you is what it is: did the AI give me autonomy I did not have on my own, or did it just move the dependency somewhere more comfortable?

## Two attempts at Linux, years apart

I had tried to switch before, more than once. The pattern was always the same: install it, get two good weeks out of it, then hit some problem (network card, video driver, printer) and fall into a search that returned forum threads from 2014, an accepted answer that did not work on my version, and a comment saying "solved it, thanks" without saying what was done. After a few hours of that, I went back to the old system.

It has now been more than two years without going back. The desktop runs Pop!\_OS and the laptop runs Ubuntu, and neither is a weekend project: that is where the work happens. What this post is after is the difference between those two phases.

## What changed was not the system

Linux did improve over those years, but not enough to explain the shift by itself. Proprietary graphics drivers still cause trouble, kernel updates still break things. What actually got shorter was the diagnostic loop. I used to have to translate my error into the vocabulary of someone who had hit something similar, and hope the search engine would bring the two close enough together. Now I hand over the exact error message, with my distribution and my version, and get back a hypothesis I can test right away. Wrong? I paste the new error and keep going. The learning curve got faster because each attempt got cheaper.

There is a caveat I cannot leave out: the AI hands back a wrong command with exactly the same confidence it hands back a right one. I have been given a flag that does not exist in the installed version, and a suggestion to touch a partition that I was not going to run without checking. Verification is still my job, and anyone who skips it has traded a night on the forums for a poorly explained `rm`.

## Linux pushes you toward free software

There is a side effect of Linux that took me a while to appreciate. When the system is free, the first solution that turns up usually is too: instead of buying a license, you go looking for the package, the script, the plugin. It is the same ground most of what I publish here comes from, QGIS and Python: someone who has already read plugin documentation to fix a projection problem is not thrown off by reading the `man` page of a system utility.

## Emancipation or a swapped dependency?

The optimistic reading has a strong case. Today I choose my operating system for what it does for me, not for how much it would cost me if something broke. That choice was not available before: the fear of getting stuck on an error kept me where I was. Gaining access to a decision that used to be off the table looks a lot like autonomy.

The suspicious reading has an equally strong case. Stack Overflow left the room and the AI took its place, and the second one is more comfortable, which makes it harder to recognize as a dependency. There is a concrete difference between them. The forum answer came stuck to somebody else's problem: the context was not mine, the version was another one, and I was forced to understand enough to adapt it. That translation work was tedious, and it was exactly where the learning happened. The AI's answer arrives fitted to my exact case, which removes the friction and, along with it, the obligation to understand.

I do not have a verdict. Both readings describe what happens to me pretty well.

## The test I use

With no verdict, what is left is a practical test I apply after the problem is fixed: did anything reusable stay behind, or was it just a pasted command? If tomorrow I can redo that on my own, or at least know where to look, it was learning. If I cannot even say what the command did, the problem simply got out of the way.

In practice this turns into two small habits. Asking for the why along with the command, because the explanation is the part that stays. And checking what the command does before running it, because verification is what separates using from obeying.

## The same dilemma in the classroom

At CEFET-MG the question arrives in a different form, with code and submitted assignments, and there it carries more weight. I see a difference that matters between two uses: students who already understand the subject use AI to go faster at something they can already do, and students who do not understand it yet use AI to skip precisely the part that teaches. The command works in both cases and the submitted work looks similar. What differs is what remains afterwards.

I still have no settled answer, for myself or for them. For now what I have is the test: look at what is left once the problem is solved.
