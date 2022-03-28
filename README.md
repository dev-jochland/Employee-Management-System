# Employee Management System
This core functionality of this project allows for a ```fictional organisation``` to make payments from the organisation's virtual wallet to their worker's virtual wallet. The project was built with the intention that it could be offered in the form of SaaS for different ```fictional organisations``` to use to manage their employees.

Assumptions for this project:
- Employees can be working for different organisations at the same time.
- Employees are added to the organisation space by the organisation's super admin or managed admins.
- An organisation super admin is created with the email provided when an organisation onboards on the platform.
- A super admin is tied to the organisation that email onboarded.
- A super admin can add other admin to help manage the organisation's activities, with different levels of permissions.
- Added admin are tied to the organisation that onboarded the admin.
- Onboarded companies are initially funded with a ``` fictional Nine hundred and ninety-nine trillion (999999999999999.00)``` coins to use.

- *```NOTE:```* Email functionality is not set up for this project, the response message is used to convey needed information for the different user actions.  

## STEPS TO RUN THIS PROJECT ON YOUR MACHINE
```NOTE:``` You need to have docker installed locally to complete the steps below.
- Clone the project to your local machine by opening your terminal and type:
```bash
git clone https://github.com/dev-jochland/Employee-Management-System.git
``` 
- ```OPTIONAL``` If you are on a MacOS or Ubuntu and your docker was not running before cloning the project, type the following command in that same terminal and provide your admin password to grant permission to run the project:
```bash
sudo chmod 666 /var/run/docker.sock
```

- While still in your terminal where you originally cloned the project, navigate into the cloned project by typing the following:
```bash
cd Employee-Management-System/
```

- Next run the following command after navigating into the project as described above:
```bash
docker-compose up
```
```NOTE```: The command above would take time to complete as it would try to build the docker image, so ensure you have a fast internet, also, you may have a "timeout error" or "HTTPconnection" error, this is as a result of your internet. Be patient as it would eventually build.

- Once the build is complete and successful, you would see the message below on your terminal: Ensure port ```1775``` is available on your local machine, to avoid port collision.
```python
web_1       | System check identified no issues (0 silenced).
web_1       | March 28, 2022 - 19:56:01
web_1       | Django version 3.2, using settings 'ems.settings.staging'
web_1       | Starting development server at http://0.0.0.0:1775/
web_1       | Quit the server with CONTROL-C.
```

```NOTE``` You need to have Postman installed locally to try out this next step.
- To try out the different endpoints available for the different type of users, you can access the [postman](https://documenter.getpostman.com/view/11396719/UVyoVxHM) documentation [here](https://documenter.getpostman.com/view/11396719/UVyoVxHM).

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)