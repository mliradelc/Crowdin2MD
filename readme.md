<!--
 Copyright (c) 2019 Maximiliano Lira Del Canto
 
 This software is released under the MIT License.
 https://opensource.org/licenses/MIT
-->

# Crowdin Top members list to Markdown script.

This script calls Markdown API to generate a list of top translators then, converts the list to markdown and save it on a desired file

# Usage:

```bash
$ Crowdin2MD.py Pidentifier Pkey -o [File]
```

- **Pidentifier**: The project identifier name.
- **Pkey**: The API key from Crowdin
- **File**: The output filename, if its none, default is `translators.md` 

## Required libraries
- requests
- beautifulsoup4

# Aknowlegments:
- [Lev Zakharov](https://github.com/lzakharov) for the `csv2md` code
- Crowdin for the translation platform