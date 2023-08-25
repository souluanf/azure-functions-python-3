from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import azure.functions as func

from routers import products
from utilities.exceptions import ApiException


description = """
Serviço responsável pela criação e alteração de usuários no AD.
"""

app = FastAPI(
    title="Active Directory API",
    description=description,
    version="0.1",
    contact={
        "name": "Luan Fernandes",
        "url": "https://linkedin.com/in/souluanf",
        "email": "luan.santos-tar@piracanjuba.com.br"
    }
)
app.include_router(products.router)
# Add additional api routers here


@app.exception_handler(ApiException)
async def generic_api_exception_handler(request: Request, ex: ApiException):
    """
    Generic API exception handler. 
    Ensures that all thrown excpetions of the custom type API Excpetion are returned 
    in a unified exception JSON format (code and description).    
    Args:
        request (Request): HTTP Request
        ex (ApiException): Thrown exception

    Returns:
        JSONResponse: Returns the exception in JSON format
    """
    return JSONResponse(
        status_code=ex.status_code,
        content={
            "code": ex.code,
            "description": ex.description
        }
    )


def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    """
    Azure function entry point.
    All web requests are handled by FastAPI.
    Args:
        req (func.HttpRequest): Request
        context (func.Context): Azure Function Context

    Returns:
        func.HttpResponse: HTTP Response
    """
    return func.AsgiMiddleware(app).handle(req, context)