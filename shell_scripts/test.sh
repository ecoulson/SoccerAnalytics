# generate images and video
i=0
count=$(find ./test_sequences -maxdepth 1 -type d|wc -l)

while [ $i -lt $1 ]
do
# create random sequence of test images
python3 ./ImageCreation.py &
wait;

ffmpeg -f image2 -r 60 -i ./test_sequences/sequence-$[$count-1+$i]/images/image-%d.png -vcodec mpeg4 -y ./test_sequences/sequence-$[$count-1+$i]/out.mp4
wait;

# analyze video and compute average position
python3 ./AveragePosition.py $[$count+$i-1] & 
wait;
# find MST from average position image
echo "script missing"
i=$[$i+1]
done
