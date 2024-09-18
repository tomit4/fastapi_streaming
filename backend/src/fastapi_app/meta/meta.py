description = """
App helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

meta_info = {
    "contact": {
        "name": "John Doe",
        "url": "https://example.com",
        "email": "johndoe@example.com",
    },
    "description": description,
    "openapi_tags": tags_metadata,
    "summary": "A Generic App",
    "terms_of_service": "https://example.com/terms/",
    "title": "App",
    "version": "0.0.1",
}
