#!/bin/bash

compiler=$1
file=$2
output=$3
addtionalArg=$4

exec  1> $"/usercode/logfile.txt"
exec  2> $"/usercode/errors"

START=$(date +%s.%2N)
if [ "$output" = "" ]; then
    $compiler /usercode/$file -< $"/usercode/inputFile" #| tee /usercode/output.txt
else
        $compiler /usercode/$file $addtionalArg #&> /usercode/errors.txt
	if [ $? -eq 0 ];	then
		$output -< $"/usercode/inputFile"
	else
	    echo "Compilation Failed"
	fi
fi
END=$(date +%s.%2N)
runtime=$(echo "$END - $START" | bc)


echo "*-COMPILEBOX::ENDOFOUTPUT-*" $runtime 
mv /usercode/logfile.txt /usercode/completed
