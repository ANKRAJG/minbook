=====
Minimal Bookmark
=====
Its a simple web apllication for adding tasks as tags(or bookmarks) called Minimal Bookmark.

Heroku Link
-----------
You can check this app by visiting: https://minbuk.herokuapp.com

Quick start
-----------

1. Add "bookmarks" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        
        'bookmarks',
    ]

2. Include the bookmarks URLconf in your project urls.py like this::

    url(r'^bookmarks/', include('bookmarks.urls')),

3. Run `python manage.py migrate` to create the bookmarks models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a tables for bookmarks (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/bookmarks/ to get started.

