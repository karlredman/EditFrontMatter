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
