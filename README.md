## miniconda3
###Setup

1. Download miniconda3
   ```
   https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
   ```
2. Install
   ```
   bash Miniconda3-latest-Linux-x86_64.sh
   ...
   Do you wish the installer to initialize Miniconda3
   by running conda init? [yes|no]
   [no] >>> yes
   ...
   ```
3. Re-login
4. Update conda
   ```
   conda update -y conda
   ```
5. Create a virtual evironment
   ```
   conda create -n vis python=3.8.5
   ```
6. Activate vis environment
   ```
   conda activate vis
   ```
7. Install packages
   ```
   pip install -r requirements.txt
   ```

### Run
conda activate vis
python app.py

### Quit
Ctrl+C

## docker-compose
### Setup
```
sudo apt install docker docker-compose
sudo usermod -aG docker $USER
# Re-login
docker-compose build
docker-compose up -d
docker-compose stop
```

### Run
docker-compose start

### Quit
docker-compose stop

### Log
docker-compose logs [-f]
