# Setup

### Requirements
- pip
- mysql

Make a copy of `conf.template.json` and rename it to `conf.json`. Now fill in the settings, needed for your environment.

To setup the project run the setup script as sudo. You can find the setup script in the `setup` folder. This will create a virtualenv, install all requirements and run the migrations.

>`sudo ./dev`

If you're deploying on a production system, execture `prod` instead. Also you should consider using a dedicated user instead of running as root.

Note that the setup scripts only supports Unix based OS'es.

# API endpoints

### Login

```[POST]		login/```
- returns a authentication token, if correct credentials are supplied.

  ######POST DATA:
  ```js
  {
  	username: <String>,
  	password: <String>
  }
  ```

### Users

```[GET]		users/(?(username))```
- lists all users

    ######PARAMS:
	- `username`: <String>
		filter by the users username. Note that usernames are unique.

```[POST]		users/```
- creates a new user

    ######POST DATA:
    ```js
    {
        /** new users username */
        username: <String>,
        /** new users password */
        password: <String>
    }
    ```

```[GET]		users/<user_id>/```
- the user with the user id `<user_id>`.

```[PATCH]		users/<user_id>/```
- change password of the user with the user id `<user_id>`.

    ######POST DATA:
    ```js
    {
        /** the users old password */
        oldPassword: <String>,
        /** the users new password */
        newPassword: <String>
    }
    ```

```[GET]		users/<user_id>/projects/```
- get all projects ot the user with the user id `<user_id>`.

```[POST]		users/<user_id>/projects/```
- add the user to an already existing project

    ######POST DATA:
    ```js
    {
        /** URL of the project you want the user to be added to */
        project: <URL>
    }
    ```

### Booking session

```[GET]		booking-session/```
- list the current booking session for the currently logged in user, in case there is an open session.

```[POST]		booking-session/```
- open a new booking session for the currently logged in user.

    ######POST DATA:
    ```js
    {
        /** timestamp of the beginning of the booking session */
        timestamp: <timestamp>
    }
    ```

```[DELETE]     booking-session/```
- close the current booking session and make the booking

### Projects

```[GET]		projects/```
- list all projects for the currently logged in user.

```[POST]		projects/```
- this endpoint is called, when a new project is created by the FAT-Client. It doesn't actually create a new project, it is just needed to update the backend, due to crappy legacy code.

    ######POST DATA:
	no post data is needed, since the information is already in the database.

```[GET]		projects/<project_id>/```
- show specific information about the project with the id `<project_id>`.

### Bookings

```[GET]		projects/<project_id>/bookings/(?(date|workpackage_id))```
- lists all bookings on this project.

	######PARAMS:
	- `date`: <date>
		if date is set, only bookings from this date will be listed. Format: YYYY-MM-DD.

	- `workpackage_id`: <int>
		if workpackage_id is set, only bookings on this workpackage will be listed.

```[POST]		projects/<project_id>/bookings/```
- creates a new booking.

	######POST DATA:
	```js
	{
		/** link to the workpackage this booking belongs to */
		workpackage: <URL>,
		/** the date of this booking. Format: YYYY-MM-DD */
		date: <date>,
		/** the workeffort in workdays (8h) */
		effort: <double>,
		/** the description of what was done */
		description: <String>
	}
	```

```[GET]		projects/<project_id>/bookings/<booking_id>/```
- lists all information regarding the booking with the booking id `<booking_id>`.

```[PATCH]		projects/<project_id>/bookings/<booking_id>/```
- updates the booking with the id `<booking_id>`. Data format is the same as for POSTs.

```[DELETE]	    projects/<project_id>/bookings/<booking_id>/```
- deletes the booking with the id `<booking_id>`.

### Workpackages

```[GET]		projects/<project_id>/workpackages/(?(topleve_wp|inactive))```
- lists all workpackages for the project with the id `<project_id>`.

    ######PARAMS:
	- `toplevel_wp`: <boolean>
		if true only toplevel workpackages are shown, if false only non toplevel workpackages.

	- `inactive`: <boolean>
		if true only inactive workpackages are shown, if false only active workpackages.

```[GET]		projects/<project_id>/workpackages/<workpackage_id>/```
- lists specific information regarding the workpackage with the id `<workpackage_id>`.

```[PATCH]		projects/<project_id>/workpackages/<workpackage_id>/```
- update the ETC of the workpackage with the id `<workpackage_id>`.

	######PATCH DATA:
	```js
	{
		/** new etc for this workpackage */
		etc: <double>
	}
	```