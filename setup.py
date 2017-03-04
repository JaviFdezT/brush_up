from setuptools import setup

setup(
  name = 'BrushUp',
  packages = ['BrushUp'], 
  version = '0.1',
  description = 'App to brush up your language skills and manage those words that you are studying in a database. Moreover, you can find an annex about pronunciation.',
  author = 'Javier Fdez. Troncoso',
  author_email = 'javierfdeztroncoso@gmail.com',
  url = 'https://github.com/JaviFdezT/brush_up', # use the URL to the github repo
  download_url = 'https://github.com/JaviFdezT/brush_up/releases/tag/0.1',
  keywords = ['english', 'pronunciation', 'game','learn'],
  install_requires=[
        "Pillow",
        "pronouncing",
        "matplotlib",
        ],
  classifiers=["Operating System :: OS Independent"],
)
