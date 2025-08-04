import math


def make_pagination(
    page_range: list[int], range_size: int, current_page: int
) -> dict[str, bool | int | list[int]]:
    if not page_range:
        return {
            "pagination": [],
            "page_range": [],
            "range_size": range_size,
            "current_page": current_page,
            "total_pages": 0,
            "start_index": 0,
            "end_index": 0,
            "first_page_out_of_range": False,
            "last_page_out_of_range": False,
    }
    if range_size <= 0:
        msg = "range_size must be greater than 0"
        raise ValueError(msg)
    if current_page < page_range[0] or current_page > page_range[-1]:
        msg = f"current_page must be between {page_range[0]} and {page_range[-1]}"
        raise ValueError(msg)

    middle_offset = math.ceil(range_size / 2)
    start_index = current_page - middle_offset
    end_index = current_page + middle_offset

    if start_index < 0:
        end_index += abs(start_index)
        start_index = 0

    if end_index >= (total_pages := len(page_range)):
        start_index = max(0, start_index - (end_index - total_pages))
        end_index = total_pages
    pagination = page_range[start_index:end_index]
    return {
        "pagination": pagination,
        "page_range": page_range,
        "range_size": range_size,
        "current_page": current_page,
        "total_pages": total_pages,
        "start_index": start_index,
        "end_index": end_index,
        "first_page_out_of_range": current_page > middle_offset,
        "last_page_out_of_range": end_index < total_pages,
    }
