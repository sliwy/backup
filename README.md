# Backup script

This is a simple script which backs up files from source directory into target directory. It saves time and resources as it does not copy all files. Instead it copies only files that changed in comparison to current directory where data is going to be placed.

## Usage
### For the first run:
1. Clone this repository or copy the `backup.py` script.
2. Use python 3 and install `tqdm` - `pip3 install tqdm`.

### Run script:
## *WATCH OUT: IF YOU SELECT THE DIRECTORIES INCORRECTLY YOUR DATA WILL BE LOST!!!*
```bash
python3 backup.py <SOURCE_DIRECTORY> <TARGET DIRECTORY>
```
- `SOURCE_DIRECTORY` is the newest version of directory you want to back up.
- `TARGET_DIRECTORY` is the directory which you want to overwrite, where the backup will be placed.

Then you have to confirm that specified directories are correctly chosen and you want to overwrite `<TARGET DIRECTORY>`. If you want to continue type `y` and  hit `ENTER`, otherwise type `n` and hit `ENTER`. 
