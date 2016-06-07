# Routes

```[GET]		users/\<user_id\>/```
- show specific information about the user with the user id \<user_id\>.

```[GET]		users/\<user_id\>/booking-sessions/```
- list the current booking session of this user, in case there is an open session.

```[POST]		users/\<user_id\>/booking-sessions/```
- open a new booking session for this user.

  ######POST DATA:
  ```js
  {
  	/** timestamp of the beginning of the booking session */
  	timestamp: <timestamp>
  }
  ```

```[DELETE]	users/\<user_id\>/booking-sessions/\<booking_session_id\>/```
- close the booking session with the id \<booking_session_id\>.

```[GET]		users/\<user_id\>/projects/```
- list all projects of the user with the id \<user_id\>.

```[GET]		users/\<user_id\>/projects/\<project_id\>/```
- show specific information about the project with the id \<project_id\>.

```[GET]		users/\<user_id\>/projects/\<project_id\>/bookings/(?(date|workpackage_id))```
- lists all bookings on this project.

	######PARAMS:
	- date:
		if date is set, only bookings from this date will be listed.

	- workpackage_id:
		if workpackage_id is set, only bookings on this workpackage will be listed.

```[POST]		users/\<user_id\>/projects/\<project_id\>/bookings/```
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

```[GET]		users/\<user_id\>/projects/\<project_id\>/bookings/\<booking_id\>/```
- lists all information regarding the booking with the booking id \<booking_id\>.

```[PATCH]		users/\<user_id\>/projects/\<project_id\>/bookings/\<booking_id\>/```
- updates the booking with the id \<booking_id\>. Data format is the same as for POSTs.

```[DELETE]	users/\<user_id\>/projects/\<project_id\>/bookings/\<booking_id\>/```
- deletes the booking with the id \<booking_id\>.

```[GET]		users/\<user_id\>/projects/\<project_id\>/workpackages/```
- lists all workpackages for the project with the id \<project_id\>.

```[GET]		users/\<user_id\>/projects/\<project_id\>/workpackages/\<workpackage_id\>/```
- lists specific information regarding the workpackage with the id \<workpackage_id\>.

```[PATCH]		users/\<user_id\>/projects/\<project_id\>/workpackages/\<workpackage_id\>/```
- update the ETC of the workpackage with the id \<workpackage_id\>.

	######PATCH DATA:
	```js
	{
		/** new etc for this workpackage */
		etc: <double>
	}
	```


```//TODO login, depending on authentication system```
