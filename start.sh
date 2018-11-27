screennode=$'cidr'
screen -S $screennode -X quit
screen -dmS $screennode
sleep 2s
cmd=$"sudo python ./cidr_worker.py"
screen -S $screennode -X stuff "$cmd"
screen -S $screennode -X stuff $'\n' 

screennode=$'ipv4'
screen -S $screennode -X quit
screen -dmS $screennode
sleep 2s
cmd=$"sudo python ./ipv4_worker.py 50"
screen -S $screennode -X stuff "$cmd"
screen -S $screennode -X stuff $'\n' 