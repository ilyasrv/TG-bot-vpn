from pyxui import XUI

# Basic:
xui = XUI(
    full_address="http://195.58.54.230:54321",
    panel="alireza", # Your panel name, "alireza" or "sanaei"
)

from pyxui.errors import BadLogin

try:
  xui.login('admin', 'admin')
except BadLogin:
  ...

get_inbounds = xui.get_inbounds()
print(get_inbounds)


get_client = xui.get_client(
    inbound_id=1,
    email="example@gmal.com",
    uuid="9d3d1bac-49cd-4b66-8be9-a728efa205fa" # Make note you don't have to pass both of them (emaill, uuid), just one is enough
)