from app import app  # Absolute import instead of relative
from app.routes import customer,  auth_routes
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="templates")

# Include the routers for different functionalities
app.include_router(auth_routes.router, prefix="/auth")
app.include_router(customer.router, prefix="/customer")


# Example route (optional)
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000)

