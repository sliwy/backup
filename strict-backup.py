# Author: Maciej Sliwowski <macieksliwowski@gmail.com>
#
# MIT License
#
# Copyright (c) 2020 Maciej Sliwowski <macieksliwowski@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import hashlib
import os
import shutil
from pathlib import Path

from tqdm.auto import tqdm


def get_hash(file_path: Path):
    return hashlib.md5(file_path.read_bytes())


def same_file(file_path, other_file_path):
    return get_hash(file_path).digest() == get_hash(other_file_path).digest()


def replace_with_source(p):
    return Path(str(p).replace(str(target_path), str(source_path), 1))


def replace_with_target(p):
    return Path(str(p).replace(str(source_path), str(target_path), 1))


parser = argparse.ArgumentParser()
parser.add_argument(
    'source_path',
    help='Source path for backup. All files and directories recursively inside '
         'the specified directory will be synchronized.')
parser.add_argument(
    'target_path',
    help='Path where all the files from source_path will be saved.')
args = parser.parse_args()
source_path = Path(args.source_path)
target_path = Path(args.target_path)

value = input(
    "Please confirm that you want to overwrite directory '"
    "{}' with files from '{}'.\ny/n\n".format(args.target_path, args.source_path))
if value != 'y':
    exit(0)

all_source_paths = list(source_path.rglob('*'))
# removing removed dirs
for path in target_path.rglob('*'):
    if replace_with_source(path) not in all_source_paths:
        try:
            if path.is_file():
                path.unlink()
        except FileNotFoundError:
            pass
for path in target_path.rglob('*'):
    if path.is_dir() and replace_with_source(path) not in all_source_paths:
        path.rmdir()

for path in tqdm(all_source_paths):
    copy_target_path = replace_with_target(path)
    if path.is_file():
        if not copy_target_path.exists():
            os.makedirs(str(copy_target_path.parent), exist_ok=True)
            shutil.copy(str(path), str(copy_target_path))
        elif copy_target_path.exists() and not same_file(path,
                                                         copy_target_path):
            copy_target_path.unlink()
            shutil.copy(str(path), str(copy_target_path))
    elif path.is_dir():
        copy_target_path.mkdir(parents=True, exist_ok=True)
