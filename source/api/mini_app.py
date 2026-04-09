# source/api/mini_app.py
"""
Mini App API — упрощённая версия (без БД)
Можно расширять постепенно:
1. ✅ Сейчас: эхо-ответ + проверка авторизации
2. 🔄 Позже: кеш в Redis
3. 🔄 Позже: запись в БД
"""

from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Any

router = APIRouter(prefix="/api/mini-app", tags=["mini-app"])


# === Простые DTO ===
class MiniAppEchoRequest(BaseModel):
    message: str = Field(default="Hello", max_length=500)
    meta: Optional[dict[str, Any]] = Field(default=None)


class MiniAppEchoResponse(BaseModel):
    ok: bool
    timestamp: datetime
    echo: str
    user_id: Optional[str] = None
    received_meta: Optional[dict[str, Any]] = None


# === Простая авторизация (только API Key для начала) ===
async def verify_api_key_simple(
    x_api_key: str | None = Header(default=None),
) -> str:
    """Проверка по простому API-ключу"""
    from source.config.config_reader import settings
    
    config_key = settings.tg.mini_app_api_key.get_secret_value()
    
    # Если ключ не настроен — разрешаем все запросы (только для разработки!)
    if not config_key:
        return "dev-mode"
    
    if not x_api_key or x_api_key != config_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return "authorized"


# === Эндпоинты ===

@router.get("/ping", tags=["health"])
async def ping():
    """Проверка доступности API"""
    return {
        "ok": True,
        "service": "mini-app-api",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }


@router.post("/echo", response_model=MiniAppEchoResponse)
async def echo_message(
    payload: MiniAppEchoRequest,
    auth: str = Depends(verify_api_key_simple),
    x_telegram_user_id: str | None = Header(default=None),
):
    """
    Простой эхо-эндпоинт для тестирования связи.
    
    В будущем здесь будет:
    - валидация данных
    - запись в Redis/БД
    - бизнес-логика
    """
    return MiniAppEchoResponse(
        ok=True,
        timestamp=datetime.utcnow(),
        echo=payload.message,
        user_id=x_telegram_user_id,  # Можно передавать из фронтенда
        received_meta=payload.meta
    )


@router.post("/save", response_model=MiniAppEchoResponse)
async def save_placeholder(
    payload: MiniAppEchoRequest,
    auth: str = Depends(verify_api_key_simple),
):
    """
    Заглушка для будущего эндпоинта сохранения.
    
    Сейчас просто возвращает подтверждение.
    В будущем: запись в базу данных.
    """
    # 🔄 Здесь позже добавим:
    # 1. Валидацию payload
    # 2. Запись в Redis (кеширование)
    # 3. Запись в PostgreSQL (постоянное хранение)
    
    return MiniAppEchoResponse(
        ok=True,
        timestamp=datetime.utcnow(),
        echo=f"[SAVED] {payload.message}",
        received_meta=payload.meta
    )

