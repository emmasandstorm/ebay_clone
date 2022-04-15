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
