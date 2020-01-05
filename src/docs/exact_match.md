**Exact Match** (`exact_match`)

Defines if the search should match the exact search term (`True`) or the string (`False`) in markdown notes. 

**Note:** When exact match is set to `True` it is possible to enhance the search term with wildcards

**Examples**

* Exact Search is enabled, search `Books` will not match `Bookstore` but `Books`. But `Books*` will match `Bookstore` as well. 
* Ecact Search is disabled, search `Books` will macht `Books` as well as `Bookstore`