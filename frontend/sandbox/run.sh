#!/bin/bash
LANGUAGE=$1
FILE=$2
INPUT=$3

# Python
if [ "$LANGUAGE" = "python" ]; then
    echo "$INPUT" | python3 "$FILE"
fi

# C
if [ "$LANGUAGE" = "c" ]; then
    gcc "$FILE" -o program.out 2>&1
    if [ $? -ne 0 ]; then exit; fi
    echo "$INPUT" | ./program.out
fi

# C++
if [ "$LANGUAGE" = "cpp" ]; then
    g++ "$FILE" -o program.out 2>&1
    if [ $? -ne 0 ]; then exit; fi
    echo "$INPUT" | ./program.out
fi
