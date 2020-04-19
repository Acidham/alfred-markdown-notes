# Alfred Markdown Notes

Markdown Notes is a comprehensive note taking tool embedded into Aflred with powerful full text search (supports & and |), tag search and search capabilities for todos ( `- [ ]` or `* [ ]`) . With MD Notes you can quickly create new notes based on custom templates, e.g. meeting notes, bookmarks, project documentation, etc. 

MD Notes works with any mardkown editor. 

> [Typora](https://typora.io/) is set up in Alfred Workflow as preferred Markdown editor but it is possible to use another MD Editor or Text Editor if required. To use another Editor it is required to define the Editor in the worklow steps at the end of the WF. 

## Installation

1. Download [Alfred Markdown Notes](https://github.com/Acidham/alfred-markdown-notes/releases/latest)
2. Double click downloaded file to install in Alfred

## Configuration

To get MD Notes to work properly it is required to define some environment variables by using the setup wizard `.mdconfig` or change the settings in Alfred Workflow Preferences: `[X]` top right corner.

### Variables

Variables marked with * are required for running MD Notes properly, the others are optional and can be set to empty.

_Note:_ Do not delete the variables!

* **Path to Notes** (`path_to_notes`): The path where MD Notes will be stored.
    The path can be absolut or relative but has to be a user directory!   
    Examples:
    * `/Users/yourname/Dropbox/Notes` →  works
    * `yourname/Dropbox/Notes` → works
    * `/yourname/Dropbox/Notes` →  works
    * `/Volumes/usb` →  will not work!
    
* **Default Date Format** (`default_date_format`): Defines date format when creating new notes or when using placeholders in templates: {date} e.g. %d.%m.%Y %H.%M

* **Default Template** * (`default_template`): The file name that will be used as default Template. Before templates can be used it is required to create the template.md e.g. `Template.md` (see [Working with Templates](#Working%20with%20Templates)) 
    **Note**: Enter the file name ONLY without path e.g. `myTemplate.md`

* **Extension** * (`ext`): The md files are text files with a specific extension (usually `.txt`or `.md`) any other extension can be defined if required.   
    **Note:** The files must be type text files.
    
* **Search in Tags in YMF only** (`search_yaml_tags_only`)
  
    Tags can be used in YAML front matter (`Tags: #mytag`) or within the MD note. 
    
    1. When set to `True` tag search only search with YMF.
    2. When set to `False` tags will be searched the whole MD note.  
    
* **Exact Match** (`exact_match`): Defines if the search should match the exact search term (`True`) or the string (`False`) in markdown notes. 

    **Note:** When exact match is set to `True` it is possible to enhance the search term with wildcards

* **URL scheme** (`url_scheme`): Some web application, like Todoist, are using a web interface where, due to OS resctrictions, file paths cannot be opened. To work around this an URL scheme can be configured to open the note in markdown editor or viewer, e.g. Marked or iA Writer. Add URL Scheme like `x-writer://create?file=` and after `file=` will be enhanced with the MD Note path when executed. 

* **Template Tag** (`template_tag`): The template tag defines which `#Tagname`) defines a Template. Once you created a template just add template tag name to the MD Note and it will be recognized when you create a new MD Note from Template (see [Create new MD Notes from Template](#Create%20new%20MD%20Notes%20from%20Template))

* **Bookmark Tag** (`bookmark_tag`): Name of the tag which marks Notes containing URL/Bookmarks.

* **Evernote Auth Token** (`evernote_auth_token`): The AuthToken for your Evernote Account. Please ensure to get non Sandbox token: [Authenticating with the Evernote Cloud API using Dev Tokens](https://dev.evernote.com/doc/articles/dev_tokens.php)

### Optional Python Packages

For exporting to evernote `markdown2`and `evernote` package is required plus Evernote and the API Key.

[https://github.com/trentm/python-markdown2](https://github.com/trentm/python-markdown2)

```bash
pip install markdown2
```

[https://github.com/evernote/evernote-sdk-python](https://github.com/evernote/evernote-sdk-python)

```bash
pip install evernote
```

### Optional: QLMarkdown

To use quicklook for Markdown files there is a QLMarkdown plugin available on git: [https://github.com/toland/qlmarkdown](https://github.com/toland/qlmarkdown)

## Features

### Full Text Search

Type `mds` keyword into Alfred and get a list of all MD files sorted by last modified date. After `mds` keyword you can type a search term and text will be searched instantly. 
The search runs with exact match and with partial match by using wildcards `*` before or after the search term

#### Syntax

* `Hello Alfred` searches for exact match of the phrase
* `Hello&Alfred` search for Notes containing the two words somewhere in the text 
* `Hello|Alfred` search for `Hello` or `Alfred` somwhere in the text
* `Book` match exact word in the text
* `Book*` machtes `Bookstore` and `Booking`
* *Tip:* You can type `#Tag` in `mds` to search for Notes with specific Tag in text and using & and | in the same way than with text search.

#### Options

With the Alfred search results from `mds` and `mdt` you can perform additional actions to the note:

* Pressing `Shift`opens Quicklook with the file. 
  *Tip*: To quicklook formatted markdown files you can install [QLMarkdown](https://github.com/toland/qlmarkdown) 
* With Pressing `CMD` you can open the action menu. The following actions are available:
  * **Markdown Link**: Copy markdown link of the note to the clipboard for pasting into another app or markdown file
  * **Delete Note**: Delete the file and all associated assets such as images or other file types. 
  * **Evernote**: Export Note to Evernote including images and tags
  	**Note:**: Only available when `evernote_auth_token` was set
  * **Marked 2**: Opens the Note in Marked 2 
      **Note:** The Markdown Editor can be changed in Alfred Preferences → Workflow
  * **URL Scheme**: Generate MD link for URL Scheme and copy to the clipboard e.g. `[My Notes](x-writer://open?path=/Users/joe/Documents/Notes/doc.md)`
  	**Note:**: Only available when `url_scheme` was set
* It is possible to perform addtional actions to one or more Notes by proceeding with File Actions (press `TAB` or `ALT+TAB` on a note or multiple notes): 
  * **Delete MD Notes**: Same as `CTRL` modifier key but also works on multiple files
  * **MD Link to Note**: Generates relative Link to a markdown document for referencing Notes in other Notes e.g. `[My Notes](mynote.md)`
  * **Create Markdown Index**: Selected Markdown files will be linked into a new Index file e.g. to collect links to all invoices for an insurance

### Tag Search

Type `md#` to get a list of all tags found in the Notes or search for Tags (see [Options](#Options) as well)

The tag search can also be used to search for already existing Tags to paste it into a markdown note. By pressing `CMD` and `Enter` the tag will be pasted into frontmost app. 

### Search in Todos

Type `mdt` to get all Todos found in the MD Notes. The list is sorted  based on when Notes with the todo was created (older notes first). As well you can search for full-text search in todo and use the modify keys (see [Options](#Options))

### Create a MD Note

#### MD Note with Title

Type `mdc` followed by a **title** to create a new MD Note with title. The default Templates will be used (see [Configuration](#Configuration))

#### Note with Title and Tags

Type `mdc`followed by **title** and **tags** separated by space will create a Note with **title** and **tags**.

#### MD Notes from Template

Type `mdc` and you get a list of all Templates in your folder. After a template was selected the title can be entered as described above.

**Note**: Templates are Notes tagged with `#Template` or whatever you defined as the template tag. 

#### YAML Fronter

MD Notes uses YAML Fronter when searching in Tags. Therefore it is required to add YAML Fronter to the top of the notes, with the following format:

```
---
Tags: #mytag
---
```

### Working with Templates

Templates are a great way to quickly create a MD Note based on a Markdown template file. The Template files are created and stored in the same way than normal notes and must contain the Template tag (see [Configuration](#Configuration)) in the YAML Fronter section (see [YAML Fronter](#YAML%20Fonter)).

There are two way to create a file based on a template:

* Via `mdc` → Create Note: A Note with a title will be created based on default template
* Via `mdc` → `Template`: The Note will be created based on selected template. After the corresponding template was selected, the title can be entered.

#### Using placeholder in Templates

The MD Notes Templates can contain two placeholder values and will be replaced when using Templates with the command `mdc`.   
With `mdc` it is also possible to directly create a note. In this case the default template will be used. The default template can be configured in Alfred Workflow settings (see [Configuration](#Configuration)):

* `{title}`: The title will be used that you entered when creating a new note 
* `{date}`: Today's date will be used when creating a new note

### Adding a file link to a Markdown Note

Images can be usually added via drag&drop to the markdown editor, esp. with Typora. It is also possible to add other file-types by using `Upload Asset for MD Notes` file action in Alfred.

To add a file to a Markdown Note, search for the File in Alfred and then press `Tab` to enter file actions. Search for `Upload Asset for MD Notes` and execute. The Markdown Link will be copied to the Clipboard. Just paste the MD Link to a Markdown Note.

### Fetch HTML Pages

MD Notes provides the possibility to fetch pages from an URL and store it in a new note. The note will be created with the containing Page title.   
In case the page cannot be fetched MD Notes create a note and add the URL into the note.

To fetch an URL use `mdf` and enter the target URL.

**Note:** To import HTML content [Pandoc](https://pandoc.org/installing.html) is required. If Pandoc is not installed the note will only contain the URL to the Page.

### Export to Evernote

MD Notes can export Notes to Evernote including Images and Tags. Once Note is shown, via `mds` choose `ALT` modifier key and Alfred shows the option ot Export to Evernote. 