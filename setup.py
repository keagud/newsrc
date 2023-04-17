from setuptools import setup

setup_opts = {
    "name": "newsrc",
    "version": "0.0.1",
    "description": "",
    "py_modules": ["newsrc"],
    "entry_points": {"console_scripts": ["newsrc=newscr/newsrc:main"]},
}

setup(

    name = "newsrc",
    version = "0.0.1",
    description="Simple template helper for single source files",
    py_modules= ["newsrc"],
    entry_points = {"console_scripts": "newsrc=newsrc:main"}



)
