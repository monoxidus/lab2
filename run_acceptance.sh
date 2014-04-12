#!/bin/bash

# uncomment for debug
# set -x

EXEC="$1"
FIXTURE_DIR="$2"

function usage {
  cat << EOF
Usage: $0 <executable> <fixture_dir>
Run acceptance tests for the given executable using the given fixture dir.
All files with extension .fx will be used as fixtures.
EOF
}

if [[ -z "$EXEC" ]]; then
    usage
    echo "ERROR: executable command was not set".
    exit 1
fi

if [ ! -d $FIXTURE_DIR ]; then
    usage
    echo "ERROR: folder "$FIXTURE_DIR" does not exist".
    exit 1
fi

make $EXEC >> "compile.log" 2>&1
rc=$?
if [[ $rc != 0 ]] ; then
    echo "ERROR: compilation of $EXEC failed."
    echo "!!! Please first compile locally and then submit."
    exit $rc
fi

echo
echo '************** Acceptance tests (using executable "'$EXEC'") **************'

VALGRIND_LOG="acceptance-valgrind.log"
rm -f "$VALGRIND_LOG"
for i in `ls "$FIXTURE_DIR"*.fx`; do
    echo
    echo '++++++ fixture '$i
    echo

    # run pexpect tests
    pexpect-fixture-runner -v 2 \
    "valgrind --leak-check=full --show-reachable=yes ./$EXEC" $i >> $VALGRIND_LOG 2>&1

    rc=$?
    if [[ $rc != 0 ]] ; then
        echo -n "ERROR: "
        echo "Acceptance tests for ./"$EXEC" failed with fixture "$i". "
        echo "See verbose output in the file "$VALGRIND_LOG
        exit $rc
    fi

    # check for invalid frees
    grep "Invalid free" -C 10 $VALGRIND_LOG > tmp.log
    rc=$?
    if [[ $rc == 0 ]] ; then
        echo -n "ERROR: There are invalid frees, please check $VALGRIND_LOG "
        echo "and search for the string \"Invalid free\""
        echo
        cat tmp.log
        exit 1
    fi

    # check for invalid writes/reads
    grep -P "Invalid read|Invalid write" -C 10 $VALGRIND_LOG > tmp.log
    rc=$?
    if [[ $rc == 0 ]] ; then
        echo "ERROR: There are invalid access to memory, please check $VALGRIND_LOG "
        echo "and search for the string \"Invalid read\" or \"Invalid write\""
        echo
        cat tmp.log
        exit 1
    fi

done

echo "OK: all acceptance test passed!"
