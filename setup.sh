if [ "$EUID" -ne 0 ]
  then echo "This script must be run as root or using sudo"
  exit
fi

echo 'Starting setup. All normal setup output is logged to setup.log'

cd "$(dirname "$0")"
> setup.log

echo 'Pulling latest version of this script...'

git pull >>setup.log

echo -e "\e[94mInstalling pip...\e[0m"
if ! type "pip" > /dev/null 2>&1; then
  python < <(curl -s https://bootstrap.pypa.io/get-pip.py) >>setup.log
fi

pip install -r requirements.txt >>setup.log 2>>setup.log

echo 'Copying configuration files...'

cp ./letter-lighting.init /etc/init.d/letter-lighting
chmod 755 /etc/init.d/letter-lighting
update-rc.d letter-lighting defaults

echo 'Starting server...'
service letter-lighting restart
