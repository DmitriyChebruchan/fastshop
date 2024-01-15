from typing import (
    Annotated,
    Union,
)

from fastapi import (
    APIRouter,
    Depends,
    Response,
    status,
)

from src.catalogue.models.database import Product
from src.catalogue.routes import (
    CatalogueRoutesPrefixes,
    ProductRoutesPrefixes,
)
from src.catalogue.services import get_product_service
from src.common.exceptions.base import ObjectDoesNotExistException
from src.common.schemas.common import ErrorResponse


router = APIRouter(prefix=CatalogueRoutesPrefixes.product)


@router.get(
    ProductRoutesPrefixes.root,
    status_code=status.HTTP_200_OK,
    response_model=list[Product],
)
async def product_list(product_service: Annotated[get_product_service, Depends()]) -> list[Product]:
    """
    Get list of products.

    Returns:
        Response with list of products.
    """
    return await product_service.list()


@router.get(
    ProductRoutesPrefixes.detail,
    responses={
        status.HTTP_200_OK: {'model': Product},
        status.HTTP_404_NOT_FOUND: {'model': ErrorResponse},
    },
    status_code=status.HTTP_200_OK,
    response_model=Union[Product, ErrorResponse],
)
async def product_detail(
    response: Response,
    pk: int,
    service: Annotated[get_product_service, Depends()],
) -> Union[Response, ErrorResponse]:
    """
    Retrieve product.

    Returns:
        Response with product details.
    """
    try:
        response = await service.detail(pk=pk)
    except ObjectDoesNotExistException as exc:
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponse(message=exc.message)

    return response