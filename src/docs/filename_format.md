**Filename Format** (`filename_format`): Standard file format for new MD notes. Default is the title of the notes but in some cases it is useful to add a date format e.g. when using Zettelkasten file format. 
The two placeholders can be used:

* e.g. `{%d-%m-%Y}` or any other strftime format. 
    ***Be careful when using strftime format. Wrong format result in wrong file names!***
* `{title}`: The title of the MD Note
* Example: `{title}-{%d%m%Y}`

