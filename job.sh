counter=1
while [ $counter -le 100000 ]
do
 python /home/iamukasa/fastdemo/artbot.py
 ((counter++))
done
echo done
