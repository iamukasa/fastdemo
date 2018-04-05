counter=1
while [ $counter -le 100000 ]
do
 python /root/fast-style-transfer-1/artbot.py
 ((counter++))
done
echo done
