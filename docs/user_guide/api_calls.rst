Make API Calls
==============

Below example demonstrate how to make an API call to `4Insight.io`_
For the complete overview of available API calls see `4Insight REST API`_. 


.. code-block:: python

    response = session.get("https://api.4insight.io/v1.0/Campaigns")

    # or with relative url

    response = session.get("/v1.0/Campaigns")


.. _4Insight REST API: https://4insight.io/#/developer
.. _4Insight.io: https://4insight.io
