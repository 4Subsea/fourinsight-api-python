Make API calls
==============

The example below demonstrates how to make an API call to `4Insight.io`_
For the complete overview of available API calls see `4Insight REST API`_. 


.. code-block:: python

    response = session.get("https://api.4insight.io/v1.1/Campaigns")

    # or with relative url

    response = session.get("/v1.1/Campaigns")


Some API endpoints support OData and have paging, which returns a default number of 50 responses per page. 
For these endpoints, the ``get_pages`` method can be useful:

.. code-block:: python

    response = session.get_pages("https://api.4insight.io/v1.1/Campaigns")
    
    # Iterate through response pages:
    for page in response:
        print(page)
    
    # Alternatively, get just the next page:
    page = next(response)


``get_pages`` returns a generator object, from which the user can iterate through the page, or obtain the pages one by one by calling ``next(response)``. 









.. _4Insight REST API: https://4insight-api-prod.4subsea.net/swagger/index.html
.. _4Insight.io: https://4insight.io
