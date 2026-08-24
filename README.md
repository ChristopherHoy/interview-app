# Python Interview

We will be continuing from where we left off at the system design interview. Here 
we have a sample application that attempts to implement what we discussed. Your goal 
here is to fix any errors you can see and to improve on the codebase to make it more 
performant, reliable, scalable and auditable. 

There is a lot to do here and you don't necessarily have to do it all, we just want to 
see how you work through the problem.


## The structure of the codebase

* `main.py`: The main entrypoint.
* `models.py`: Contains Pydantic models that define the structure of our API.
* `integration.py`: Contains clients for connecting to upstream providers.
* `routes.py`: The business logic for our endpoint
* `provider/`: Contains a sample provider for testing, this always returns a success

You will also note that in the docker compose file we have a localstack deployment. 
This is to facilitate the use of queues if you want to get to it in this interview.