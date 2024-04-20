# build_files.sh
pip3 install -r requirements.txt
python3.10 manage.py collectstatic --noinput