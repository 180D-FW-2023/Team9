#!/bin/bash

fifo_path="fifo264.txt"

if [ -p "$fifo_path" ]; then
    echo "Removing existing $fifo_path"
    rm "$fifo_path"
fi

mkfifo "$fifo_path"
echo "Starting stream on $fifo_path"
Ncat -l -v -p 5777 | cat > "$fifo_path"
