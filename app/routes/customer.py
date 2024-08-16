from fastapi import APIRouter, Request, Depends, Form, HTTPException
from .. import templates, get_db
from bson import ObjectId
from pymongo.errors import PyMongoError
from ..models import AddToCartRequest, CartItem
from ..auth import get_current_user
router = APIRouter()

@router.get("/dashboard")
def customer_dashboard(request: Request, db=Depends(get_db),
                       user: str = Depends(get_current_user)):
    """
    Serve the customer dashboard with a list of available fruits.

    Args:
        request (Request): The request object.
        db: The MongoDB database session.

    Returns:
        TemplateResponse: The rendered customer dashboard HTML page.
    """
    try:
        # Fetch fruits data from the 'fruits_details' collection
        fruits_cursor = db["fruits_details"].find({})
        fruits = []
        for fruit in fruits_cursor:
            fruit['_id'] = str(fruit['_id'])  # Convert ObjectId to string
            fruits.append(fruit)

        return templates.TemplateResponse("customer_dashboard.html", {
            "request": request,
            "username": user,
            "fruits": fruits
        })
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post("/add_to_cart")
async def add_to_cart(
        request: Request,
        cart_request: AddToCartRequest,
        db=Depends(get_db), user: str = Depends(get_current_user)
):
    """
    Add selected fruits to the cart for the hardcoded user.

    Args:
        cart_request (AddToCartRequest): The request data containing selected fruits.
        db: The MongoDB database session.

    Returns:
        dict: A success message indicating the fruits were added to the cart.
    """
    try:
        if not cart_request.items:
            raise HTTPException(status_code=400, detail="No fruits selected")

        purchase_data = []

        for item in cart_request.items:
            fruit = db["fruits_details"].find_one({"_id": ObjectId(item.fruit_id)})
            if not fruit:
                raise HTTPException(status_code=404, detail=f"Fruit with id {item.fruit_id} not found")

            purchase_data.append({
                "fruit_id": ObjectId(item.fruit_id),
                "name": fruit['name'],
                "price": fruit['price'],
                "quantity": item.quantity,
                "total_cost": item.quantity * fruit['price'],
                "user_id": user,
            })

        # Insert the purchase data into the 'purchase_details' collection
        db["purchase_details"].insert_many(purchase_data)

        return {"message": "Selection added to cart successfully"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.get("/view_cart")
def view_cart(
        request: Request,
        db=Depends(get_db), user: str = Depends(get_current_user)
):
    """
    View the current cart contents for the hardcoded user.

    Args:
        request (Request): The request object.
        db: The MongoDB database session.

    Returns:
        TemplateResponse: The rendered summary HTML page with the cart contents.
    """
    try:
        # Fetch the purchase details for the hardcoded user
        purchase_details = db["purchase_details"].find({"user_id": user})

        total_cart_price = 0
        fruits = []

        for detail in purchase_details:
            total_cart_price += detail['total_cost']
            fruits.append(detail)

        return templates.TemplateResponse("summary.html", {
            "request": request,
            "fruits": fruits,
            "total_cart_price": total_cart_price
        })
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")


@router.post("/clear_cart")
def clear_cart(request: Request, db=Depends(get_db), user: str = Depends(get_current_user)):
    """
    Clear the cart for the hardcoded user.

    Args:
        db: The MongoDB database session.

    Returns:
        dict: A success message indicating the cart was cleared.
    """
    try:
        # Remove all documents from the 'purchase_details' collection for the hardcoded user
        db["purchase_details"].delete_many({"user_id": user})

        return {"message": "Cart cleared successfully"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")
