File Management
===============


Opening Files
-----------------


The file browser and File menu enable you to work with files and
directories on your system. This includes opening, creating, deleting,
renaming, downloading, copying, and sharing files and directories.

The file browser is in the left sidebar Files tab:

.. image:: images/file_menu_left.png
   :align: center
   :class: jp-screenshot
   :alt: Arrow pointing to the file browser in the upper left sidebar.

Many actions on files can also be carried out in the File menu:

.. image:: images/file_menu_top.png
   :align: center
   :class: jp-screenshot
   :alt: A screenshot showing the File menu open including options like "New", "Save All."

.. _open-file:

To open any file, double-click on its name in the file browser:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/Rh-vwjTwBTI?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _newtab:

You can also drag a file into the main work area to create a new tab:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/uwMmHeDmRxk?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _multiple-viewers:

Many files types have :ref:`multiple viewers/editors <file-and-output-formats>`.
For example, you can open a Markdown file in a :ref:`text editor <file-editor>` or as rendered HTML.
A JupyterLab extension can also add new viewers/editors for files.
To open a file in a non-default viewer/editor, right-click on its name in the
file browser and use the "Open With..." submenu to select the viewer/editor:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/1kEgUqAeYo0?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _single-doc-sync:

A single file can be open simultaneously in multiple viewer/editors and
they will remain in sync:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/87ALbxm1Y3I?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _file-navigation:

The file system can be navigated by double-clicking on folders in the
listing or clicking on the folders at the top of the directory listing:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/2OHwJzjG-l4?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _file-share:

Right-click on a file or directory and select "Copy Shareable Link" to
copy a URL that can be used to open JupyterLab with that file or
directory open.

.. image:: images/shareable_link.png
   :align: center
   :class: jp-screenshot
   :alt: A screenshot showing the Copy Shareable Link option in the context menu opened over a file, which is the last entry on the list.

.. _file-copy-path:

Right-click on a file or directory and select "Copy Path" to copy the
filesystem relative path. This can be used for passing arguments to open
files in functions called in various kernels.

Creating Files and Activities
-----------------------------

.. _file-create-plus:

Create new files or activities by clicking the ``+`` button at the top
of the file browser. This will open a new Launcher tab in the main work area,
which enables you to pick an activity and kernel:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/QL0IxDAOEc0?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _file-create-menu:

You can also create new documents or activities using the File menu:

.. image:: images/file_create_text_file.png
   :align: center
   :class: jp-screenshot
   :alt: A screenshot showing the context menu entry for creating a new file.

.. _current-directory:

The current working directory of a new activity or document will be the
directory listed in the file browser (except for a terminal, which
always starts in the root directory of the file browser):

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/OfISSOTiGTY?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _file-rename:

A new file is created with a default name. Rename a file by
right-clicking on its name in the file browser and selecting “Rename”
from the context menu:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/y3xzXelypjs?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

Uploading and Downloading
-------------------------

.. _file-upload:

Files can be uploaded to the current directory of the file browser by
dragging and dropping files onto the file browser, or by clicking the
"Upload Files" button at the top of the file browser:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/1bd2QHqQSH4?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _file-download:

Any file in JupyterLab can be downloaded by right-clicking its name in
the file browser and selecting “Download” from the context menu:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/Wl7Ozl6rMcc?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

Displaying Hidden files
-----------------------

If the hidden files are allowed by the Administrator, then you will be able to display or hide the hidden files through the menu View -> Show Hidden Files.


Important folders
-----------------

While working in Notebooks, it is important to keep in mind the folder
structure. When logging into Notebooks, users see two folders in the
file browser on the left: ``shared`` and ``work``.

-  ``shared`` folder is the symbolic link to ``/opt/shared``, which is
   reserved for shared storage across all apps. Currently, there are two
   folders inside of ``shared``: ``notebooks`` and ``wipp``.

   -  ``notebooks`` is the shared folder for all users of notebooks
      across the deployemnt. That allows to store some common notebooks,
      code and datasets and collaborate on them with other users of
      Notebooks
   -  ``wipp`` contains file storage for WIPP, including Image
      Collections, CSV collections, registered notebooks, Stitching
      vectors and Pyramids. Keep in mind that this folder is in the
      read-only mode; if you need to add new image collection, please
      use WIPP UI.

-  ``work`` is the users’ persistent storage. All files in that folder
   will persist the notebook restarts and is the place to keep your
   work.

All the files and folders created in the home folder outside of
``shared`` and ``work`` will be deleted on notebook restart, which
happen after a period of inactivity (15-60 minutes).

Uploading and Downloading
-------------------------

.. _file-upload:

Files can be uploaded to the current directory of the file browser by
dragging and dropping files onto the file browser, or by clicking the
"Upload Files" button at the top of the file browser:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/1bd2QHqQSH4?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

.. _file-download:

Any file in JupyterLab can be downloaded by right-clicking its name in
the file browser and selecting “Download” from the context menu:

.. raw:: html

  <div class="jp-youtube-video">
     <iframe src="https://www.youtube-nocookie.com/embed/Wl7Ozl6rMcc?rel=0&amp;showinfo=0" frameborder="0" allow="autoplay; encrypted-media" allowfullscreen></iframe>
  </div>

Deleting folders
----------------

To protect users from accidentaly deleting the folder, JupyterLab made a
decision to block non-empty folder deletion with right-click
(https://github.com/jupyterlab/jupyterlab/issues/835). Unfortunately,
until the issue is fixed, you would have to delete everything from
inside the folder manually *or* use the Termianl to delete the folder.
In Terminal you can run the command: ``rm -rf <folder_path>`` to delete
the folder.