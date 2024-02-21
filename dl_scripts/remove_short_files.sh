#!/usr/bin/env bash

# Assuming the list of files is provided as command-line arguments
for file in "$@"; do
  baseName=$(basename "$file")
  # Check if file starts with "Wikipedia"
  if [[ "$baseName" == Wikipedia* ]]; then
    echo "Removing $file because it starts with 'Wikipedia'"
    rm -- "$file"
    continue
  fi

  # Count the number of words in the file
  word_count=$(wc -w < "$file")

  # Check if the word count is fewer than 10
  if [ "$word_count" -lt 10 ]; then
    echo "Removing $file because it has fewer than 10 words"
    rm "$file"
  fi
done

