Logging
#######

:py:mod:`fourinsight.api` allows for detailed logging of API calls.
For instance, outputing the log to ``stdout`` can be done in the following manner::

    import logging
    from sys import stdout

    from fourinsight.api import UserSession

    logger = logging.getLogger("fourinsight.api")
    logger.setLevel("DEBUG")

    handler = logging.StreamHandler(stdout)
    logger.addHandler(handler)

    session = UserSession()
    response = session.get("/v1.0/Campaigns")


If you require even more detailed logging, consider using loggers from
:py:mod:`requests`, :py:mod:`oauthlib`, and :py:mod:`requests-oauthlib`.