from fastapi import Request


def is_logged_in(request:Request):
    return request.state.user is not None