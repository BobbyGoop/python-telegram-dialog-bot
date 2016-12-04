import collections.abc
import functools


def require_choice(caption, table, question=None):
    """
    Requires user to make a choice of given set of options.

    Args:
        caption (String) - message to send with table of choices
        table (Union[Iterable[String], Iterable[Iterable[String]]]) - choices
        question (Optional[String]) - message to send when wrong answer given

    Returns:
        Union[Integral, Tuple[Integral, Integral]] - index of chosen option
        String - text of chosen option
    """
    choices = table
    if not isinstance(table[0], str):
        choices = sum(table, [])
    question = question or caption
    answer = yield ((caption, table) if caption else table)
    while answer.text not in choices:
        answer = yield(question)
    if not isinstance(table[0], str):
        return next(
            (row_idx, row.index(answer.text))
            for row_idx, row in enumerate(table)
            if answer.text in row
        ), answer
    else:
        return table.index(answer.text), answer


def requires_personal_chat(error_message):
    """
    Make dialog generator work in personal chats only.

    Args:
        error_message (String) - message to send when addressed in group chat

    Returns:
        Decorator
    """

    def decorator(func):

        @functools.wraps(func)
        def result_func(message):
            chat_id = message.chat_id
            sender_id = message.from_user.id
            if chat_id != sender_id:
                yield error_message
                return
            result = yield from func(message)
            return result

        return result_func

    return decorator