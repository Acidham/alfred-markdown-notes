**URL Scheme** (`url_scheme`): I figured out that some web application like Todoist are implemented as a web interface and due to OS restrictions file paths cannot be opened. To work around the restrictions a URL Scheme  for MD editors help to open the Note in e.g. Marked 2 or iAWriter.

**Example by using Marked 2:**
Marked is using the URL scheme `x-marked://open/?file=<file_path>`. To set value for `url_scheme` in configuration you need to add `x-marked://open/?file=`