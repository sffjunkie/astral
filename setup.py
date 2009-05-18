try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(name='astral',
    version='0.01',
    description='Calculations for dawn, sunrise, solar noon, sunset and dusk.',
    author='Simon Kennedy',
    author_email='astral@sffjunkie.co.uk',
    url="http://www.sffjunkie.co.uk/python-astral.html",
    license='MIT',
    py_modules=['astral'],
    install_requires=['pytz']
)

