# create an image
docker build --tag test-img .

# run the app
docker run --name test-cntnr test-img

# clean up
docker ps -a
docker rm -f test-cntnr
