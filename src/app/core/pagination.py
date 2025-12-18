from fastapi import HTTPException, Query


def get_page_params(
    page_number: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
) -> tuple[int, int]:
    if page_size > 50:
        raise HTTPException(400, detail="page_size cannot exceed 50")
    return page_number, page_size
