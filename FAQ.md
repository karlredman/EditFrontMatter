# FAQ

EditFrontMatter: Frequently Asked Questions

## Are these answers actually frequently asked?

Probably not. I'm preempting some of the answers that I thought might be useful or interesting.

## Why is this project so heavily / distractingly / etc. documented?

Fist of all, the irony is not lost on me here:

I'm documenting a `python` module, using `reST` through [Sphinx](https://www.sphinx-doc.org/en/master/), that I wrote in order to edit markdown front matter in [GFM](https://github.github.com/gfm/) files that I will be using for distributing [Hugo](https://gohugo.io/) documentation. Whereby Hugo is written in `golang`. And BTW, the files I am building with Hugo are all created through [vimwiki](https://vimwiki.github.io/)!

When I started documenting this project it was the first time I'd worked with Sphinx. My initial intentions were to just create some short document pages for [Read The Docs](https://readthedocs.org/). That led me to figuring out how to host the static pages on Github Pages. Then I realized that I wanted to create a boilerplate thing using the [Sphinx RTD Theme](https://sphinx-rtd-theme.readthedocs.io/en/stable/); which became a side project on it's own..

All the while I was trying to mix / coordinate the RTD theme, Sphinx (native), and pydoc documentation so that nothing looked too out of place. After some time I realized that I might as well add example programs to further test the Sphinx documentation system and my little project / module here. This led me to a workflow that cycled through a) working on coding, b) trying to document the code, c) attempting to boilerplate the documentation system, and d) back to coding. This led to minimal customizations of the RTD Theme configuration, which fed the coding possibilities, and the boilerplate concept, etc.

## Why did you write this module?

I needed a simple python script that would walk a directory tree and format the 'edit this page' links in the Hugo front matter of my markdown pages so that they correctly point to my running [Gitea](https://gitea.io/en-us/) instance properly. Later, I decided to use this module as a learning experience / experiment. And now we have this.

## Where is the test suite!?

I changed the testing harness smack dab in the middle of developing the examples and then got side tracked with building the documentation stuff. I will add the test suite back into the mix at a future date.
