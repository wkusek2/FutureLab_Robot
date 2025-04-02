###################################
# Copy necessary files from repo  #
# to Jetson Nano via ssh          #
###################################

# jetson address
jetson_name=orin
jetson_address=192.168.55.1
jetson_host=$jetson_name@$jetson_address

# copying method selection
jetson_key=$1
command="-i ${jetson_key}"

# open ssh connection if no key specified
if [ -z $jetson_key ]; then
    command="-o ControlPath=ssh-conn"
    ssh -fMNS ssh-conn -o ControlPersist=yes $jetson_host
fi

ssh $command $jetson_host "mkdir -p ~/podwodny &&
                            mkdir -p ~/podwodny/src &&
                            mkdir -p ~/podwodny/utils &&
                            mkdir -p ~/podwodny/utils/packages"
scp $command -r *.py $jetson_host:~/podwodny/
scp $command -r src/* $jetson_host:~/podwodny/src/
scp $command -r utils/opencv-cuda/* $jetson_host:~/podwodny/utils/
scp $command -r utils/packages/* $jetson_host:~/podwodny/utils/packages/
ssh $command $jetson_host "chmod +x ~/podwodny/utils/installer.sh"
ssh $command $jetson_host "chmod +x ~/podwodny/utils/packages/install-packages.sh"

echo "--------------------------------"

# close ssh connection
if [ -z $jetson_key ]; then
    ssh -S ssh-conn -O exit $jetson_host
fi

echo [+] All project files copied to Jetson.
exit 0
