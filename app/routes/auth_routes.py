from fastapi import APIRouter, HTTPException, Depends,Request
from fastapi.responses import JSONResponse
from ..auth import create_access_token, verify_password,get_password_hash
from ..models import LoginData,UserCreate
from .. import get_db
from pymongo.errors import PyMongoError
from .. import templates

router = APIRouter()

# GET route to serve the login page
@router.get("/login")
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login(login_data: LoginData, db=Depends(get_db)):
    try:
        # Fetch the user from the 'user' collection
        user = db["users"].find_one({"username": login_data.username})
        if not user or not verify_password(login_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate JWT token
        access_token = create_access_token(data={"sub": login_data.username})

        return JSONResponse({"access_token": access_token, "token_type": "bearer"})
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")

@router.post("/register")
async def register_user(user_data: UserCreate, db=Depends(get_db)):
    try:
        # Check if the user already exists
        if db["users"].find_one({"username": user_data.username}):
            raise HTTPException(status_code=400, detail="Username already taken")

        # Hash the user's password
        hashed_password = get_password_hash(user_data.password)

        # Create the new user with the hashed password
        new_user = {
            "username": user_data.username,
            "password": hashed_password
        }

        # Insert the new user into the database
        db["users"].insert_one(new_user)

        return {"message": "User registered successfully"}
    except PyMongoError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {e}")