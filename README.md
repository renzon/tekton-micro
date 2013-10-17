ZenWArch
========

Zen Web Architecture - A engine to routing by convention

Inside the project source code there is a folder called "project_template"

You can use it as a template for your app. It is running, as example, on http://zenwarchi.appspot.com

navigate to project_template/src/venv and run 

```
./venv.sh
```

It will build a virtualven on the venv folder and create a symlink on src, so Google App Engine can see the your libraries.

You can run this command again this anytime you want to add or upgrade a lib on requirements.txt

You need python 2.7 to be installed on your computer and the [Google App Engine SDK](https://developers.google.com/appengine/downloads)
 
After adding the SDK in your path, you can navigate to project_template/src and run the command:

```
dev_appserver.py . --port=8088
```

This command will start the local server on localhost:8088

The framework documentation is on github wiki: https://github.com/renzon/zenwarch/wiki

The lib is available on pypi:

```
pip install zenwarch
```
