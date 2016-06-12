# Setup

To setup the project run the setup script as sudo. You can find the setup script in the `setup` folder. This will create a virtualenv and install all requirements.

>`sudo ./dev`

If you're deploying on a production system, execture `prod` instead.

Afterwards, make a copy of `conf.template.json` and rename it to `conf.json`. Now fill in the settings, needed for your environment.


# Routes

```[POST]		login/```
- returns a authentication token, if correct credentials are supplied.

  ######POST DATA:
  ```js
  {
  	username: <String>,
  	password: <String>
  }
  ```

```[GET]		booking-sessions/```
- list the current booking session for the currently logged in user, in case there is an open session.

```[POST]		booking-sessions/```
- open a new booking session for the currently logged in user.

  ######POST DATA:
  ```js
  {
  	/** timestamp of the beginning of the booking session */
  	timestamp: <timestamp>
  }
  ```

```[DELETE]     booking-sessions/<booking_session_id>/```
- close the booking session with the id `<booking_session_id>`.

```[GET]		projects/```
- list all projects for the currently logged in user.

```[POST]		projects/```
- this endpoint is called, when a new project is created by the FAT-Client. It doesn't actually create a new project, it is just needed to update the backend, due to crappy legacy code.

    ######POST DATA:
	no post data is needed, since the information is already in the database.

```[GET]		projects/<project_id>/```
- show specific information about the project with the id `<project_id>`.

```[GET]		projects/<project_id>/bookings/(?(date|workpackage_id))```
- lists all bookings on this project.

	######PARAMS:
	- `date`:
		if date is set, only bookings from this date will be listed.

	- `workpackage_id`:
		if workpackage_id is set, only bookings on this workpackage will be listed.

```[POST]		projects/<project_id>/bookings/```
- creates a new booking.

	######POST DATA:
	```js
	{
		/** the id of the workpackage this booking belongs to */
		workpackageId: <int>,
		/** the date of this booking. Format: YYYY-MM-DD */
		date: <date>,
		/** the workeffort in hours */
		workEffort: <double>,
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

```[GET]		projects/<project_id>/workpackages/```
- lists all workpackages for the project with the id `<project_id>`.

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