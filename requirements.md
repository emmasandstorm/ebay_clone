## Functional Requirements

1.  Users can login to access their account and to buy, sell, and bid on items \*Emma
2.  Users can logout \*Emma
3.  New users can create an account to buy, sell, and bid on items \*Cathy
4.  Logged in users can delete their account \*Cathy
5.  Users can add items to a cart to purchase all in one batch \*Emma
6.  Users can buy items with a credit/debit card \*Evan
7.  Users can search for item by name or seller \*Emma
8.  Users can place bids on items listed for auction \*Evan
9.  Users can list items on the seller store and choose a between a flat price or auction \*Evan
10. Users can add image to items they list on the store \*Evan
11. Users can navigate to a page that displays all items available from all sellers \*Cathy
12. User accounts include user profiles with names and editable biographies \*Cathy

## Non-functional Requirements

1. Consistent cool color theme
2. System can persist up to 1000 listings
3. Images can only be of one file type
4. Posts can have up to 256 characters

## Use Cases

5. Add item to Cart

- **Summary:**
  Customer can select an item and it is added to their cart for purchase later

- **Actor:**
  Customer

- **Pre-conditions:**
  Customer must be logged in

- **trigger:**
  Customer selects 'Add to cart' button

- **Primary Sequence:**

  1.  Intended item is entered into search box
  2.  All entries relevant to the search is displayed
  3.  Customer selects intended item
  4.  Description and image of item is displayed
  5.  Customer selects 'Add to Cart' button
  6.  Item is added to cart for purchase later

- **Alternative Sequence:**

  1.  Item is not available for purchase
  2.  Error message pops up
  3.  Customer is returned to item description page

- **Post Conditions:**

  - Item is in cart and can be viewed and edited
  - Item is ready for purchase

- **Non-functional requirements:**

  - Item added to cart within 1 second

- **Glossary:**
  - customer: a person who is using the ebay clone website to purchase something
  - cart: the list of items that a customer has compiled to purchase at a later time
  - item: something that is being sold on the website

7. Find Item

- **Summary:**
  A text entry displays all relevant items

- **Actor:**
  Customer

- **Pre-conditions:**
  None

- **trigger:**
  Submit button is pressed after a text entry is inputted into search bar

- **Primary Sequence:**

  1.  The item query is entered into the search bar
  2.  The Submit button is pressed
  3.  A query is sent through all available items and looks for keywords from the text entry in item descriptions
  4.  A list of all items containing relevant data to the text query is displayed

- **Alternative Sequence:**

        1. Text query does not have any relevant items

  2.  Error message pops up informing customer of issue
  3.  Customer is prompted to enter a more relevant item

- **Post Conditions:** - List of relevant items is displayed

- **Non-functional requirements:**

        - List is displayed within 2 seconds for each 100 items

  - Items can be filtered by price or relevance _keywords_

- **Glossary:** - customer: a person who is using the ebay clone website - search bar: text entry box at the top of the page used for searching - item: something that is being sold on the website

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

11. See All Items for Sale

- **Pre-condition:** None

- **Trigger:** User selects "Shop All" button.

- **Primary Sequence:**

  1. System redirects the user to the shop page. Items are displayed in order of being available
  2. User is able to scroll through all available items

- **Primary Postconditions:** User can log in to actually purchase items from "Shop All"

- **Alternate Sequence:**

  1. User logs in as a customer
  2. System redirects the user to the shop page.
  3. Customer goes to the "Shop All" page and is able to add items to their cart

12. Edit User Profile

- **Pre-condition:** User must be logged in.

- **Trigger:** User selects "My Profile" button

- **Primary Sequence:**

  1. System redirects the user to their personal profile page
  2. User selects "Edit Display Name" button
  3. System prompts the user to enter a new display name of less than 30 characters
  4. User enters their new display name and selects "Save Name"
  5. System saves their new display name and updates the profile page to show it

- **Primary Postconditions:** The user's profile is updated based on the edits they make

- **Alternate Sequence:**

  1. System redirects the user to their personal profile page
  2. User selects "Edit Bio" button
  3. System prompts the user to enter a new bio of less than 150 characters
  4. User enters thier new bio and selects "Save Bio"
  5. System saves their new display name and updates the profile page to show it
