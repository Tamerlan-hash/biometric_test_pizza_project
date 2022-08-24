from fastapi import APIRouter, Depends

from modules.pagination import Page, paginate
from modules.dal import DAL, get_dal

from app.schemas import RestaurantOut
from app.models import Restaurant

pizza_router = APIRouter(tags=["Pizza"])







