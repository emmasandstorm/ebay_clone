# Buying

Buying a listing consists of searching for a listing, examining its details on the listing page, adding to cart (include quantity), viewing cart, and checking out. You are also capable of seeing all past listings that you have purchased. 

## Finding Listings

Description of finding listings for purchase

## Cart

Once on a listing description page, if that item is still available for purchase, an Add to Cart button is on the page along with a number entry box for quantity. The user can then choose the quantity and add the item to the cart. 
    How it works:
    1. Add to Cart pressed
    2. Item and it's info is turned into a dictionary
    3. That dictionary is added into a session key 'Shoppingcart'
    4. If any other items are added to cart, those dictionaries are added as well
    5. Removing an item removes the dictionary out of the session dict
    6. Adding an item that is already on the cart triggers a warning that says the item is already in the cart.
The cart will be saved as long as the user stays signed in. 

A user can view their cart by adding an item to their cart or pressing the cart button on the navbar. The cart pulls each value from the corresponding key in the listing dictonatary for viewing. On the cart viewing page, the grandtotal of the items is calculated and there is an option to continue shopping (redirects to home page) or to go to checkout (redirects you to checkout page).

## Checkout

On the checkout page, simply enter fake credit card information (please do not use a real card) and confirm your purchase. All items in your cart will be purchased, remove from cart, and updated to proudly display your ownership.


## Purchased Listings

View all the listings you own
