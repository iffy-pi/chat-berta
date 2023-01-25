This contains files used by React and Flask, it is located here to support React Imports.

We keep it synced with the use of hard links (see more in main README)

# How I Did It
First I created the shared-linked directories in src/ and apiutils.

Then I created a hard link for the config.json file, for both locations
```
mklink /h apiutils\shared-linked\config.json shared-linked\config.json
mklink /h src\shared-linked\config.json shared-linked\config.json
```

Then I added both files to git and then pushed.

# Adding More files
To add more files, you just have to create the hard links