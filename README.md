# pyblish-manager
🎵 do it like they do it on the VA-LI-DA-TION channel 🎵

![gif of the tool in action](docs/pyblish_manager_demo.gif)

a simple browser to visualise your current pyblish registration state.
great for debugging, or quickly adding new paths to test new plugins. 
hurray for browsing!

to spawn in maya:
```python
import manager_GUI_widget as w
#import pyblish_register_types as reg
#reload(reg)
#reload(w)
widget = w.make_config(qapp=False)
```

to spawn externally:
```python
import manager_GUI_widget as w
widget = w.make_config(qapp=True)
```