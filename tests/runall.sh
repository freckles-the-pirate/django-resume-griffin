ALL_TESTS=$(find -iname 'test*.py')
for t in $ALL_TESTS; do
    TEST_NAME=$(echo $t | sed 's/\.py//' | sed 's/\.\///' | sed 's/\//\./')
    ./runtests.sh $TEST_NAME;
done;
