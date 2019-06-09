---
title: "EditFrontMatter Class Example 3"
description: "Edit 2 fields in this front matter"
catagories: [programming, python, markdown]

deleteme: this will be deleted

tags: [front matter, administration, testing]

# comments and spaces will be eliminated (see docs)

author: "Karl N. Redman"
creatordisplayname: "Karl N. Redman"
creatoremail: "karl.redman@example.com"
date: 2019-05-23T17:43:45-05:00
lastmodifierdisplayname: "Karl N. Redman"
lastmodifieremail: "karl.redman@gmail.com"
lastmod: 2019-05-23T17:43:45-05:00
toc: false
type: "page"
hasMath: false
draft: false
weight: 5


# EditFontMatter Class Example 3

Edit several fields of front matter.

## Fields affected in this example:

* toc
  * note: uses local template variable
  * pre: false
  * post: true
* draft:
  * note: uses jinja2 filter (callback)
  * pre: false
  * post: true
* hasMath
  * note: uses program variable
  * pre: true
  * post: false
* stuff:
  * note: uses program variable to create field
  * pre: did not exist
  * post: (list) ['one', 'two', 'three']
* deleteme:
  * note: removed from final result
  * pre: this will be deleted
  * post: N/A
