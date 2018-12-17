# session-scripts
A collection of Python scripts for working with Sedeen session files.

## Author Join

This script joins session files created by different authors into a single session file. The options are below:
```
usage: Join sedeen session files produced by multiple authors
       [-h] [-v] [-o OUTPUT_DIR] [-c] dir

positional arguments:
  dir                   path to source directory containing author subfolders

optional arguments:
  -h, --help            show this help message and exit
  -v, --verbose         increase output verbosity
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        directory to store output session file
  -c, --color-by-author
                        override color by author
```

Here's an example usage:
```
python scripts\author_join.py path\to\data -v -c
```

In this example, `path\to\data` contains subfolders with the names of the authors. Each subfolder would contain a session file. It would look something like this:
```
path\to\data
├── Dr. House\
│   └── sample.session.xml
├── Dr. Wilson\
│   └── sample.session.xml
└── Dr. Taub\
    └── sample.session.xml
```

The `-v` option turns on verbose output so you can debug any problems. The `-c` option strips the existing colors in each session file and adds new colors to help distinguish annotations by author.


