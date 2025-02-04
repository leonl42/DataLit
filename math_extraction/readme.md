Extracts the math and saves it in the format: 

```
(Chapter, tex)
(Chapter, tex)
.
.
.
(Chapter, tex)
```

Chapter is a set of numbers separated by dots, where each number represents the depth of a chapter. E.g. "3.2.4" would represent the 4th subsubchapter in the 2nd subchapter in the 3rd chapter.

The script can be run via:

```
bash main.sh
```

after entering the paths and potentially adjusting the other parameters. Note that absolute paths are necessary. Tex path is the path to the folder with the tex file. Save path is the path to the folder where the parsed math shall be saved. Note that log files will be deposited inside the Tex path folder. The output file will be named "parsed.math" inside the Save path folder. If no file was generated, the parser was not able to parse the file. Example: