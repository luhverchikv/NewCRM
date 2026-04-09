# source/api/mini_app.py
from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional, Any

from source.database.core import DatabaseSession, get_db_session
from source.database.models.base import BaseRecord
from source.enums.roles import UserRole
from aiogram.utils.web_app import check_webapp_signature

router = APIRouter(prefix="/api/mini-app", tags=["mini-app"])


# === DTO ===
class MiniAppDataCreate(BaseModel):
    user_id: str = Field(..., min_length=1, description="Telegram ID пользователя")
    data: dict[str, Any] = Field(..., description="Данные от mini-app")
    source: Optional[str] = Field(default="web", description="Источник: web/telegram")
    
    @validator('user_id')
    def user_id_must_be_numeric(cls, v):
        if not v.isdigit():
            raise ValueError('user_id должен быть числом (Telegram ID)')
        return v


class MiniAppDataResponse(BaseModel):
    id: int
    user_id: str
    created_at: datetime
    status: str = "saved"
    
    class Config:
        from_attributes = True


# === Авторизация ===
# source/api/mini_app.py
from fastapi import Header, HTTPException, status

async def verify_mini_app_request(
    x_api_key: str | None = Header(default=None),
    x_telegram_init_data: str | None = Header(default=None),
) -> dict:
    from source.config.config_reader import settings  # ← Импорт глобального settings
    
    # 1. Проверка API Key (если настроен)
    config_key = settings.tg.mini_app_api_key.get_secret_value()
    
    if config_key and x_api_key == config_key:
        return {"auth_method": "api_key"}
    
    # 2. Если ключ не настроен — разрешаем только Telegram initData
    if not config_key and not x_telegram_init_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="API key not configured. Use Telegram initData for auth."
        )
    
    # 3. Проверка Telegram initData (безопасный способ)
    if x_telegram_init_data:
        try:
            bot_token = settings.tg.bot_token.get_secret_value()
            from aiogram.utils.web_app import check_webapp_signature
            
            if check_webapp_signature(bot_token, x_telegram_init_data):
                from aiogram.utils.web_app import parse_webapp_init_data
                user_data = parse_webapp_init_data(x_telegram_init_data)
                return {
                    "auth_method": "telegram",
                    "user": user_data.user,
                    "user_id": str(user_data.user.id)
                }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid Telegram initData: {str(e)}"
            )
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Missing or invalid authentication"
    )



# === Эндпоинты ===

@router.post("/save", response_model=MiniAppDataResponse, status_code=201)
async def save_mini_app_data(
    payload: MiniAppDataCreate,
    auth: dict = Depends(verify_mini_app_request),
    db: DatabaseSession = Depends(get_db_session)
):
    """Сохранить данные из mini-app в общую БД"""
    
    # Используем user_id из Telegram initData, если доступен (безопаснее)
    user_id = auth.get("user_id", payload.user_id)
    
    # Создаём запись
    record = BaseRecord(
        user_id=user_id,
        data=payload.data,
        source=payload.source,
        created_at=datetime.utcnow()
    )
    
    db.add(record)
    await db.commit()
    await db.refresh(record)
    
    return MiniAppDataResponse.model_validate(record)


@router.get("/history/{user_id}", response_model=list[MiniAppDataResponse])
async def get_user_history(
    user_id: str,
    auth: dict = Depends(verify_mini_app_request),
    db: DatabaseSession = Depends(get_db_session),
    limit: int = Query(50, ge=1, le=200)
):
    """Получить историю записей пользователя"""
    
    # Проверка: пользователь может видеть только свои данные
    # (или админ может видеть все)
    auth_user_id = auth.get("user_id")
    if auth_user_id and auth_user_id != user_id:
        # Проверяем, админ ли это (нужна ваша логика)
        # if not await is_admin(auth_user_id):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    from sqlalchemy import select
    from source.database.models.base import BaseRecord
    
    records = await db.execute(
        select(BaseRecord)
        .where(BaseRecord.user_id == user_id)
        .order_by(BaseRecord.created_at.desc())
        .limit(limit)
    )
    
    return [
        MiniAppDataResponse.model_validate(r)
        for r in records.scalars().all()
    ]

