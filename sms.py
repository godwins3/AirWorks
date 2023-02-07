# import package
import africastalking


# Initialize SDK
username = "sandbox"    # use 'sandbox' for development in the test environment
api_key = "0400606da5dc0bb3c11596d85d645b5f419c2e845b766750b22d8b8f0d6a5a34"      # use your sandbox app API key for development in the test environment
africastalking.initialize(username, api_key)


# Initialize a service e.g. SMS
sms = africastalking.SMS


# Use the service synchronously
response = sms.send("Hello Message!", ["+254742079321"])
print(response)

# Or use it asynchronously
def on_finish(error, response):
    if error is not None:
        raise error
    print(response)

sms.send("Hello Message!", ["+254742079321"], callback=on_finish)    
