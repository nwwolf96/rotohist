def parse_int_or_zero(value: str | None) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0
