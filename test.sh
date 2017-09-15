# generate images and video
i=0

while [ $i -lt $1 ]
do
./shell_scripts/createSequence.sh &
sleep 1000 &
i=$[$i+1]
done

# analyze video and compute average position

# find MST from average position image