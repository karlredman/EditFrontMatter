## Example 2 markdown

This file will be processed normaly and then concatinated with `example`.md

* Changes in output of example1.md:
* weight
  * note: uses local template variable
  * pre: 5
  * post: 10
* draft:
  * note: uses jinja2 filter (callback)
  * pre: true
  * post: none
* stuff:
  * note: deleted from yaml
  * pre: (list) ['one', 'two', 'three']
  * post: N/A

