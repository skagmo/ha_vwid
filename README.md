# Volkswagen ID component for Home Assistant

This folder contains both a generic Python 3 library for the Volkswagen ID API and a component for Home Assistant using the library.

## Home Assistant component installation

* (Activate We Connect using the official app)
* Add content of "custom_components/vwid" in this repository to the custom_components subfolder in your Home Assistant configuration folder
  * Home assistant has to be restarted
* Go to integrations and search for "Volkswagen ID"
* Fill in username/email, password and VIN as used in your app
* There should now be a sensor entity called "sensor.state\_of\_charge" with a lot of attributes with the remaining values

## Library

"custom\_components/vwid/libvwid.py" contains the Python class to communicate with the We Connect ID API used by the ID series electric cars. See libvwid_example.py in the same folder for usage.


