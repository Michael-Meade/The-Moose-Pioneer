# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /

# copy the dependencies file to the working directory
COPY requirements.txt .

# install dependencies
RUN pip3 install -r requirements.txt \ 
    git clone https://github.com/yanxiu0614/subdomain3.git \
    cd subdomain3 \
    pip3 install -r requirement.txt

# copy the content of the local src directory to the working directory
COPY / .

# command to run on container start
CMD [ "python", "./nmaps.py" ]
