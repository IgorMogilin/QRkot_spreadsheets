from datetime import datetime


def fund_project(target, sources):
    """Функция, реализующая логику инвестирования"""
    changed_objects = []
    for source in sources:
        free_from_source = source.full_amount - source.invested_amount
        if free_from_source <= 0:
            continue
        need_for_target = target.full_amount - target.invested_amount
        if need_for_target <= 0:
            break
        to_invest = min(free_from_source, need_for_target)
        source.invested_amount += to_invest
        target.invested_amount += to_invest
        if (
            source.invested_amount >= source.full_amount and
            not source.fully_invested
        ):
            source.fully_invested = True
            source.close_date = datetime.utcnow()
        if (
            target.invested_amount >= target.full_amount and
            not target.fully_invested
        ):
            target.fully_invested = True
            target.close_date = datetime.utcnow()
        if source not in changed_objects:
            changed_objects.append(source)
        if target not in changed_objects:
            changed_objects.append(target)
        if target.fully_invested:
            break
    return changed_objects
