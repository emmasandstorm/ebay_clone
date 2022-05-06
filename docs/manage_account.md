# Account Management

The user system is a database that consists of a user id, user submitted username and password. The password automatically generates a password_hash that is used to check the password when logging in.

Also included in the user database is the relationship of being a buyer. Once a customer makes a purchase, their user id is tied to that listing and they're now marked as the buyer of the listing. This allows the user to view all past purchases (coming soon).

## Create Account

Users create new accounts from the signup page. Choose a unique username and any password, then press Register. Your credentials will be stored in the database, and now you can log in!

## Delete Account

Account deletion coming soon

## Login

Navigate to /login page by clicking the Login button in the top Navbar. Additionally, if you try to access any page that requires a login, it will redirect you to the login page to log you in. Once on the Login Page, you must enter your:

- Username (saved in the database from original sign up on create account page)
- Password (assigned a password_hash so it can be checked in the database with the original password assigned to the account)

Once your credentials have been entered, hit the submit button. This will tell the system to find a unique username that matches the entered username that already exists in the database. If it matches, it will then check the password to see if it matches the assigned password_hash.

If there is any issue with the login or the credentials don't match, an error message will flash, telling you there was an error.

If everything is matching, the system will log you in and grant you access to much of the website.

## Logout

You must be logged in to logout.

To logout, you must press the logout button on the navbar. It will redirect you to a logout page. If you are not logged in, you will be redirected to the login page so you can logout. If you are logged in, the system will log you out of the session and take you back to the login page.

## User Profile

How to view and edit your own user profile (coming soon).
