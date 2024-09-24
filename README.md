To install dependencies run
```angular2html
$ pip install -r requirements.txt
```

To run application
```angular2html
guinicorn app:app
```

To run local server in debug mode
```angular2html
$ flask --app app --debug run
```
Register an email address and password then log in as a regular user. You can edit your detail from the home page then log out.

To Login as Admin the login details are
```
Email = admin@example.com
Password = password
```
On the ViewUsers page you can select which user you would like to edit by clicking on the user.
You can then edit user details or permanently delete a user record.

On the SeachUsers page you can search all users by their skills. Enter 1 or more skills.
Note: The more skills you enter the less likely you will get a user matching all those skills. 

To run unit tests
```
$ python3 -m pytest
```

To prettify and format code changes


```angular2html
& pip install djlint && black
$ djlint . --reformat
$ black .
```

