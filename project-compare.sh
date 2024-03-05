#/bin/bash

# Find the most recently modified file in the utils folder
# of each of my reactpy projects

# ./project-compare.sh | sort

for dir in ../reactpy*
do
    if [ -d "$dir" ]; then
        if [ -d "$dir/utils" ]; then
            ls -tl  ${dir}/utils/*.py | head -n1
        fi

    fi
done
