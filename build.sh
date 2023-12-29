 echo "BUILD START"
sudo apt install libcairo2-dev pkg-config python3-dev
 python3.9 -m pip install -r requirements.txt
 python3.9 manage.py collectstatic --noinput --clear
 python3.9 manage.py migrate
 echo "BUILD END"
