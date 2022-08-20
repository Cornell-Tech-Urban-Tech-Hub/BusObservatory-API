# rebuild each time
# pip install wheel will overcome the build fail error
sam build --use-container && sam local start-api --debug
# sam build && sam local start-api --debug
