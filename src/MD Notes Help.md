---
Created: 03.02.2019
Tags: #Draft #Alfred #Help
---

# MD Notes Help for Alfred

Markdown Notes help to manage Markdown files in a directory with powerful full text search (supports & and |), tag search or search for todos ( `- [ ]` or `* [ ]`) . It also allows to quickly create new notes based on custom templates. 

> [Typora](https://typora.io/) is set up in Alfred Workflow as preferred Markdown editor but it is possible to use another MD Editor or Text Editor if required. To use another Editor it is required to define the Editor in the worklow steps at the end of the WF. 

## Configuration

To get MD Notes to work properly it is required to define some environment variables by using the setup wizard `.mdconfig` or change the settings in Alfred Workflow Preferences: `[X]` top right corner.

### Variables

Variables marked with * are required for running MD Notes properly, the others are optional and can be ignored.

* **Path to Notes** *  (`path_to_notes`): The path where markdown files store will be stored. The path needs to be relative to your home directory e.g. your notes are stored in `/Users/yourname/Dropbox/Notes` then the path to add to the configuration will look like `/Dropbox/Notes`
* **Default Template** * (`default_template`): The file that will be used as default Template. Before templates can be used it is required to create the template.md e.g. `Template.md` (see [Working with Templates](#Working%20with%20Templates)) 
* **Extension** * (`ext`): The md files are text files with a specific extension (usually `.txt`or `.md`) any other extension can be defined if required.   
**Note:** The files must be type text files.
* **URL scheme** (`url_scheme`): I figured out that some web application like Todoist are using web interface where, due to OS resctrictions, file paths cannot be opened. To work around this URL scheme can be configured to open the note in markdown editor or viewer, e.g. Marked or iA Writer. Add URL Scheme like `x-writer://create?file=` and after `file=` will be enhanced with the MD Note path when executed. 
* **Template Tag** (`template_tag`): The template tag defines which `#Tagname`) defines a Template. Once you created a template just add template tag name to the MD Note and it will be recognized when you create a new MD Note from Template (see [Create new MD Notes from Template](#Create%20new%20MD%20Notes%20from%20Template))
* **Bookmark Tag** (`bookmark_tag`): Name of the tag which marks Notes containing URL/Bookmarks.
* **Evernote Auth Token** (`evernote_auth_token`): The AuthToken for your Evernote Account. Please ensure to get non Sandbox token: [Authenticating with the Evernote Cloud API using Dev Tokens](https://dev.evernote.com/doc/articles/dev_tokens.php)

### Required Python Packages

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

#### Syntax

* `Hello Alfred` search for exact match of the two words in MD Notes
* `Hello&Alfred` search for Notes withthe two words in the the text 
* `Hello|Alfred` search wether `Hello` or `Alfred` in MD Notes
* *Tip:* You can type `#Tag` to search for Notes with specific Tag in text and using & and | in the same way than with text search.

#### Options

With the Alfred search results from `mds` and `mdt` you can perform additional actions to the note:

* Pressing `Shift`you can quicklook the file. 
  *Tip*: To quicklook markdown files formatted you can install [QLMarkdown](https://github.com/toland/qlmarkdown) 
* Pressing `CMD` will copy the Markdown file link for pasting into another app or markdown file
* Pressing `ALT` export formatted note to Evernote. (Not available in `mdt`)
	**Note:** Tags will be exported to Evernote as well. 
* Pressing `CTRL` will delete the file and all associated assets such as images or other file types. 
* Pressing `FN` will open the Note in Marked 2 or any other defined Markdown Editor/Viewer
  **Note:** The Markdown Editor can be changed in Alfred Preferences → Workflow
* It is possible to perform addtional actions to one or more Notes by proceeding with File Actions (press `tab` on a note): 
  * **Delete MD Notes**: Same as `CTRL` modifier key but also works on multiple files
  * **Copy URL Scheme MD Link**: Generate MD link for URL Scheme e.g. `[My Notes](x-writer://open?path=/Users/joe/Documents/Notes/doc.md)`
  * **MD Link to Note**: Generates relative Link to a markdown document for referencing Notes in other Notes e.g. `[My Notes](mynote.md)` 

### Tag Search

Type `md#` to get a list of all tags found in the Notes or search for Tags (see [Options](#Options) as well)

### Search in Todos

Type `mdt` to get all Todos found in the MD Notes. The list is sorted  based on when Notes with the todo was created (older notes first). As well you can search for full-text search in todo and use the modify keys (see [Options](#Options))

### Create new MD Notes

Type `mdc` followed by a title to create a new MD Note with title. The default Templates will be used (see [Configuration](#Configuration))

### Create new MD Notes from Template

Type `mdc` and you get a list of all Templates in your folder: 
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

### Export to Evernote

MD Notes can export Notes to Evernote including Images and Tags. Once Note is shown, via `mds` choose `ALT` modifier key and Alfred shows the option ot Export to Evernote.