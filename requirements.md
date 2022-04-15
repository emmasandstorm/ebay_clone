## <remove all of the example text and notes in < > such as this one>

## Functional Requirements

1. requirement
2. requirement
3. requirement
4. requirement
5. requirement
6. requirement
7. requirement
8. requirement
9. requirement
10. requirement
11. requirement
12. requirement

## Non-functional Requirements

1. non-functional
2. non-functional
3. non-functional
4. non-functional

## Use Cases

1. Bid on listings within auction window.

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

  4. Add an image to a listing when creating that listing

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
