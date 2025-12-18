import uuid
from math import ceil
from typing import Optional

from fastapi import (
    APIRouter,
    Depends,
    File,
    Form,
    HTTPException,
    Query,
    UploadFile,
    status,
)
from sqlalchemy import func
from sqlalchemy.orm import Session

from src.app.core.auth import get_current_user
from src.app.core.pagination import get_page_params
from src.app.db.models.article import Article
from src.app.db.models.category import Category
from src.app.db.models.deleted_article import DeletedArticle
from src.app.db.models.user import User
from src.app.db.session import get_db
from src.app.schemas.article import (
    ArticleOut,
    ArticleUpdate,
    PaginatedArticles,
)
from src.app.services.s3 import upload_image

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=PaginatedArticles)
def list_articles(
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    page_params: tuple[int, int] = Depends(get_page_params),
):
    page_number, page_size = page_params

    query = db.query(Article)

    if category_id is not None:
        query = query.filter(Article.category_id == category_id)

    if search:
        search_expr = func.to_tsvector("simple", Article.title + " " + Article.text)
        query = query.filter(search_expr.match(search))

    total = query.count()
    items = (
        query.order_by(Article.created_at.desc())
        .offset((page_number - 1) * page_size)
        .limit(page_size)
        .all()
    )

    total_pages = ceil(total / page_size) if total else 1

    return PaginatedArticles(
        items=items,
        page_number=page_number,
        page_size=page_size,
        total=total,
        total_pages=total_pages,
    )


@router.post(
    "",
    response_model=ArticleOut,
    status_code=status.HTTP_201_CREATED,
)
async def create_article(
    title: str = Form(...),
    text: str = Form(...),
    category_id: int = Form(...),
    image: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=400, detail="Category does not exist")

    image_url: Optional[str] = None
    if image is not None and image.filename:
        ext = image.filename.rsplit(".", 1)[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        image_url = upload_image(image.file, filename, image.content_type or "image/*")

    article = Article(
        title=title,
        text=text,
        category_id=category_id,
        image_url=image_url,
        author_id=current_user.id,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.put("/{article_id}", response_model=ArticleOut)
async def update_article(
    article_id: int,
    payload: ArticleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    if payload.title is not None:
        article.title = payload.title
    if payload.text is not None:
        article.text = payload.text
    if payload.category_id is not None:
        category = db.query(Category).filter(Category.id == payload.category_id).first()
        if not category:
            raise HTTPException(status_code=400, detail="Category does not exist")
        article.category_id = payload.category_id

    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_article(
    article_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")

    if article.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Forbidden")

    deleted = DeletedArticle(
        original_id=article.id,
        title=article.title,
        text=article.text,
        image_url=article.image_url,
        category_id=article.category_id,
        author_id=article.author_id,
        created_at=article.created_at,
        updated_at=article.updated_at,
    )
    db.add(deleted)
    db.delete(article)
    db.commit()
    return
