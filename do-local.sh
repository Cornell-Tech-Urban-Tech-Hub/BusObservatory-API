# ## hot reload 
# ## per https://stackoverflow.com/questions/69977480/using-aws-sam-cli-requires-rebuild-every-time-i-update-the-code
# sam local start-api --skip-pull-image

# rebuild each time
sam build --use-container && sam local start-api --debug
