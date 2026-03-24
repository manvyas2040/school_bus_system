"""Utility functions for the application."""


def paginate(page: int = 1, page_size: int = 10) -> tuple[int, int]:
    """Normalize pagination parameters.
    
    Args:
        page: Page number (1-based)
        page_size: Number of items per page
        
    Returns:
        Tuple of (page, page_size) with validated values
    """
    page = max(page, 1)
    page_size = min(max(page_size, 1), 100)
    return page, page_size
