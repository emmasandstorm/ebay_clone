## Functional Requirements

1. Login
2. Logout
3. Create new account
4. Delete account
5. Add item to Cart *Emma
6. Buy item
7. Find item *Emma
8. Bid on items *Evan
9. Add item to seller store
10. Add image to item* *Evan
11. See all items available from all of the sellers *Cathy
12. User profiles *Cathy

## Non-functional Requirements

1. Consistent cool color theme
2. System can persist up to 1000 listings
3. Images can only be of one file type
4. Posts can have up to 256 characters

## Use Cases

5. ~ Name~ Add item to Cart
~ Summary ~ Customer can select an item and it is added to their cart for purchase later
~ Actor ~ Customer
~ Pre-conditions ~ Customer must be logged in
~ trigger ~ Customer selects 'Add to cart' button
~ Primary Sequence ~
	1. Intended item is entered into search box
	2. All entries relevant to the search is displayed
	3. Customer selects intended item
	4. Description and image of item is displayed
	5. Customer selects 'Add to Cart' button
	6. Item is added to cart for purchase later
~ Alternative Sequence ~
	1. Item is not available for purchase
	2. Error message pops up
	3. Customer is returned to item description page
~ Post Conditions ~
	- Item is in cart and can be viewed and edited
	- Item is ready for purchase
~ Non-functional requirements ~ 
	- Item added to cart within 1 second
	- Add to cart button shown on listing as well as description page
~ Glossary ~
	- customer: a person who is using the ebay clone website
	- cart: the list of items that a customer has compiled to purchase at a later time
	- item: something that is being sold on the website

7. ~ Name ~ Find Item
~ Summary ~ A text entry displays all relevant items
~ Actor ~ Customer 
~ Pre-conditions ~ Customer must be logged in
~ trigger ~ Enter key is pressed after a text entry is inputted into search bar
~ Primary Sequence ~
        1. Customer logs in
	2. The item query is entered into the search bar
	3. The Submit button is pressed
	4. A list of all items containing relevant data to the text query is displayed
~ Alternative Sequence ~
        1. Text query does not have any relevant items
	2. Error message pops up informing customer of issue
	3. Customer is prompted to enter a more relevant item
~ Post Conditions ~
        - List of relevant items is displayed
~ Non-functional requirements ~ 
        - List is displayed within 2 seconds for each 100 items
	- Items can be filtered by price or relevance *keywords*
~ Glossary ~
        - customer: a person who is using the ebay clone website
        - search bar: text entry box at the top of the page used for searching
        - item: something that is being sold on the website

8. Bid on listings within auction window.

- **Pre-condition:**
  User must be logged in, must have a valid credit card associated with their account, and must navigate to a listing.
  The listing must have bidding enabled, and the auction time window must still be open.

- **Trigger:**
  User clicks on place bid button.

- **Primary Sequence:**

  1. System prompts the user to enter a price at least $.01 above previous bid
  2. User enters bid in text box and clicks submit
  3. System validates user input and attempts to place the bid
  4. If the bid is successful, confirms successful bid to the user.

- **Primary Postconditions:**
  List of bids for this listing has been updated to reflect the new bid. User is financially responsible to pay the bid
  if no higher bid is placed by the end of the auction window.

  OR

  No bid was placed and nothing in the system is changed.

- **Alternate Sequence:**

  1. The user's bid is not higher than the current bid.
  2. System updates the current bid and notifies the user of the issue.
  3. System prompts the user for a new bid.

- **Alternate Sequence:**

  1. The user decides not to place a bid.
  2. The user clicks the cancel button.
  3. The user is redirected to the listing (as appropriate/necessary).

10. Add an image to a listing when creating that listing

- **Pre-condition:**
  User must be logged in
  User must be on the page for creating a listing

- **Trigger:**
  User presses "Add image" button

- **Primary Sequence:**

  1. System prompts user for an image of the appropriate type and size.
  2. User submits image and presses upload button
  3. System validates the file and stores the valid image on the server.
  4. User is redirected to the listing page, where the image is now displayed

- **Primary Postconditions:**
  New image is stored in the system, appropriate link to the listing in the database

  OR

  No file is added and listing contains no image

- **Alternate Sequence:**

  1. File is too large
  2. File is rejected and user is prompted to submit a smaller file
  3. System validates the file and stores the valid image on the server.
  4. User is redirected to the listing page, where the image is now displayed

- **Alternate Sequence:**

  1. File is wrong type
  2. File is rejected and user is prompted to submit a file of the appropriate type
  3. System validates the file and stores the valid image on the server.
  4. User is redirected to the listing page, where the image is now displayed

  - **Alternate Sequence:**

  1. User chooses not to submit a file
  2. User clicks on the cancel button
  3. User is redirected to the listing page, where the default empty image is displayed
