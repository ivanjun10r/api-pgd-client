from typing import Any

from .. import namedtuples
from ..constants import headers as constants_headers


def authorization_header_factory(
    str_value: str = "", **kwargs: Any
) -> namedtuples.HeaderItem:
    value = str_value if str_value else constants_headers.AUTHORIZATION_HEADER.value
    return namedtuples.HeaderItem(
        constants_headers.AUTHORIZATION_HEADER.name, value.format(**kwargs)
    )


def header_item_factory(
    header_item: namedtuples.HeaderItem, value: str = "", **kwargs: Any
) -> namedtuples.HeaderItem:
    value_ = value if value else header_item.value
    return namedtuples.HeaderItem(header_item.name, value_.format(**kwargs))


def create_headers_with(header_items: list[namedtuples.HeaderItem]) -> dict[str, str]:
    try:
        return {item.name: item.value for item in header_items}
    except AttributeError as exc:
        raise Exception(
            "All header items should be a api_pgd_client.namedtuples.HeaderItem object"
        ) from exc
