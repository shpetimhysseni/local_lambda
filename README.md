# Zip Service
Rubik Backend App microservice.

## Set up

Follow the steps below to setup the project before starting to develop.

Create a virtual environment and activate it:

```
virtualenv venv
source venv/Scripts/activate
```

Install the dependencies for the project:

```
pip install -r requirements.txt
```

For the app to run locally, execute the following command:
```
python -m app.app
```

## Deployment

Service is deployed on **FaaS** (Function as a Service) model in AWS using lambda function. To make things easier from
writing code to deployment we use `serverless` framework. 

This lambda uses a docker image which is built by using the Dockerfile and pushed to AWS
by executing the `push_image.sh`. 

The lambda is deployed to `dev/prod` by executing `deploy_to_dev.sh/deploy_to_prod.sh`


## Pattern of the services

Zip Service is deployed in the domain:

- production - api.rubikhomes.com
- development - devapi.rubikhomes.com <br/>

Zip service creates an API mapping over the API Gateway. The service is mapped on the API
Gateway with the prefix of `/zip_service` specifically `api.rubikhomes.com/user_service`, and then all the other
request would be redirected to this subroute.

## References for the tools

* [Serverless framework](https://www.serverless.com/)
* [Lambda functions](https://docs.aws.amazon.com/lambda/latest/dg/welcome.html)


