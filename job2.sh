counter=1
while [ $counter -le 10000000000 ]
do
nohup python /home/iamukasa/fastdemo/fbbot.py
 ((counter++))
done
echo done
