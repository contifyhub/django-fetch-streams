=====
fetch_stream
=====

fetch_stream is a Django app to connect to a stream source and receive data and store in

Quick start
-----------

1. Add "fetch_stream" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'fetch_stream',
    ]

2. Include the fetch_stream URLconf in your project urls.py like this::

    path('fetch_stream/', include('fetch_stream.urls')),

3. Run ``python manage.py migrate`` to create the fetch_stream models.

4. You can register the related fetch_stream models to any existing app admin or create custom admin file to render the related admin apps

5. Start the development server and visit http://127.0.0.1:8000/admin/
   to view the fetch_stream related data (you'll need the Admin app enabled).

