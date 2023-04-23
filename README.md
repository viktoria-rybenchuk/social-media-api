# Social Media Api

This API allows users to perform various actions related to social media, including adding comments, following and unfollowing other users, deleting comments, and posting photos.

## Installing using GitHub:

```
git clone git@github.com:viktoria-rybenchuk/social-media-api.git

python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate

```
### Load data from fixture
```
python manage.py loaddata social_media_db_data.json
python manage.py runserver

```

## Getting access
 1. create user via/api/user/register/
 2. get access token via/api/user/token/

## Features

Add comments to posts
 - Follow and unfollow other users
 - Delete comments from posts
 - Post photos to user profiles
 - Create new posts with titles and content
 - Edit user account information
 - Update and delete posts (only the author has permission)
 - Update and delete comments (only the author has - permission)
 - JWT authenticated
 - Admin panel/admin
 - Documentation is located at /api/doc/swagger/
 - Filtering use and username

## Conclusion

This Social API rovides a set of endpoints that allow users to perform various actions related to social media, such as adding comments, following and unfollowing other users, deleting comments, and posting photos. By following the steps in this README file, you can quickly get started using the API to build your own social media applications.
