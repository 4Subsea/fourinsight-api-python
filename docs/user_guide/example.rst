Use case example
================

Here are two simple examples showing how you can use the API endpoints to access data. The first example demonstrates how to find all instruments associated with a field, and the second example demonstrates how to find all risers with a specified length and sort them by field.

To build your own application using your desired API endpoints, you can find a complete overview of the available API endpoints in the `4insight REST API`_ documentation.

.. caution::
    Do not use the INTERNAL API endpoints. You can however use the endpoints from version 1.0, 1.1 and 1.2.

.. code-block:: python
    
    from fourinsight.api import UserSession

    session = UserSession()

    #Find the FlexTrackEntityId of the field
    field_name = "INSERT FIELD NAME HERE"
    field_url = f"https://api.4insight.io/v1.1/FieldsLookups?%24filter=Title%20eq%20%27{field_name}%27"
    field = session.get(field_url).json()
    field_id = field['value'][0]['FlexTrackEntityId']

    #Find all instruments associated with the field
    instruments_url = f"https://api.4insight.io/v1.1/Instruments?%24filter=FlexTrackFieldEntityId%20eq%20{field_id}"
    instruments = session.get(instruments_url).json()
    all_instruments = instruments['value']

.. code-block:: python

    from fourinsight.api import UserSession

    session = UserSession()

    # Set length of riser to filter by
    length_riser = 800

    # Find all risers with the specified length and sort them by field
    riser_url = f"https://api.4insight.io/v1.1/Risers?%24filter=Length%20eq%20{length_riser}"
    riser = session.get(riser_url).json()['value']
    sorted_risers = sorted(riser, key=lambda x: x['FlexTrackFieldEntityId'])

    # Find the field associated with each riser
    risers_with_fields = []
    for riser in sorted_risers:
        field_id = riser['FlexTrackFieldEntityId']
        field_url = f"https://api.4insight.io/v1.1/FieldsLookups?%24filter=FlexTrackEntityId%20eq%20{field_id}"
        try:
            field_title = session.get(field_url).json()['value'][0]['Title']
            riser["Field"] = field_title
        except:
            riser["Field"] = "Field not found"
        risers_with_fields.append(riser)

Additionally, here is a video on how to authorize and obtain the URL for the endpoint you wish to use, found under `Request URL`. 

.. video:: fig/swagger.mp4
    :width: 800
    :height: 600

.. _4insight REST API: https://4insight-api-prod.4subsea.net/swagger/index.html


