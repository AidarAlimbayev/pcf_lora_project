#!/bin/bash

PROGRAM="kramer"

function test {
    ANSWER=$(echo $1 | ./$PROGRAM)
    if [ "$ANSWER" != "$2" ]; then
        echo "in: $1 exp: $2 out: $ANSWER"
    fi
}

test "1 0 0 1 3 3" "2 3 3"
test "1 1 2 2 1 2" "1 -1 1"
test "0 2 0 4 1 2" "4 0.5"
test "2 3 4 6 1 2" "1 -0.666667 0.333333"
test "0 1 0 3 5 15" "4 5"
test "1 0 1 0 3 3" "3 3"
test "0 1 0 2 1 1" "0"
test "0 0 0 0 0 1" "0"
test "0 0 0 0 1 0" "0"
test "0 0 0 0 0 0" "5"
test "0 1 0 -1 0 0" "4 0"
test "1 -1 0 -1 1 0" "2 1 -0"
test "0 0 1 2 0 3" "1 -0.5 1.5"
test "0 0 1 -2 0 1" "1 0.5 -0.5"
test "1 -2 0 0 1 0" "1 0.5 -0.5"
test "0 0 0 1 0 1" "4 1"