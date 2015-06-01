Django résumé Griffin
=====================

Purpose
-------

So, you're wanting to put up a résumé on your site (being an excellent
Django developer and all, why not?). You grab your good ol' PDF you've
used since 2007 and copy and paste your résumé in the WYSIWYG editor in
Django. It may look pretty; you may have to mess with it a little bit.

Yeah, you could do it that way. Or you could do it **the Griffin Way!**

Django résumé Griffin takes your résumé to the next level by modelling
it. You can keep track of where you worked, for how long, and who your
managers were.

### What's With the Name?

A lot of open source projects use a gimmick to name projects or
versions. The naming scheme for my projects is mythical creatures. This
one is--obviously--a griffin. My other projects include [Token
Asena](https://www.pypy.org/griffin-token-asena) and [Project
Goblin](https://www.pypi.org/django-project-goblin).

Installation
------------

As with most django apps, the easiest way way is PIP:

    pip install -U django-resume-griffin

Now add `griffin` to the list of installed apps:

    INSTALLED_APPS = (
        # ...
        'griffin',
        # ...
    )

Features
--------

### Project Goblin Plugin

Because I'm always up for a little self-promotion I included a plug-in
to Project Goblin. Note that résumé Griffin checks to see if Project
Goblin is installed. If it is, then a model to include a Project Goblin
Project is available in the admin interface.

The `GoblinProject` model is only a wrapper model. The real Project
Goblin `Project` model is in the models' `project` attribute. So, to
access the Project Goblin project from résumé Griffin in a template, do
this:

    <h2>{{ project.project.name }}</h2>
    <p class="description">{{ project.project.description }}</p>

### Convert For Download

Because reStructuredText is just awesome, résumé Griffin makes it easy
to convert your resume to various formats.

Simply go into the **résumé Formats** app and create a new format. When
you want to add a download link to the page, use the template tag like
this:

    {% load ... resume %}

    {% resume_download_links resume [ formats ... ] %}

`resume` is the resume passed in to the context for the template. The
`formats` are optional and will default to all résumé formats available
for the given résumé. For example:

    {% resume_download_links resume "pdf" "odt" %}

Will render links to download the résumé in pdf and odt format.

#### The reStructuredText Template

résumé Griffin uses a reStructuredText template to convert to various
formats.

To override the template, simply copy the `download.rst` file from the
`$GRIFFIN_SOURCE/griffin/tempaltes/resume/` directory (or roll your own)
and place it in your project's `templates/resume/` directory.

If you do override the template, just be careful that you respect the
syntax and structure of reStructuredText (e.g. spaces, new lines, etc.)

#### Pandoc Support

During installation or configuration you may have run into an error with
PanDoc. Unfortunately, some servers may not have PanDoc support. *Some*
conversion support is made possible with the `docutils` package, but it
won't have as near the amount of support as PanDoc.

résumé Griffin will automatically detect in PanDoc is installed. If it's
not, then résumé Griffin will try to convert using `docutils` or...

If you find you don't have PanDoc and you need a super-awesome file
format, you can provide it when you add résumé Downloads.

