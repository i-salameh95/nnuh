import re

from menus.base import Modifier
from menus.menu_pool import menu_pool

from cms.models import Page

class GenerateReverseIdModifier(Modifier):
    """
    This modifier makes the changed_by attribute of a page
    accessible for the menu system.
    """
    def modify(self, request, nodes, namespace, root_id, post_cut, breadcrumb):
        try:
            if root_id and root_id.startswith('page_autogen_reverse_id__') and not post_cut and not breadcrumb:
                page_id = re.findall('\d+', root_id)[0]
                print("-"*100, page_id)
                # only consider nodes that refer to cms pages
                # and put them in a dict for efficient access
                # page_nodes = {n.id: n for n in nodes if n.attr["is_page"]}
                node = [n for n in nodes if n.id == int(page_id)][0]
                if not node.attr.get('reverse_id', None):
                    node.attr['reverse_id'] = root_id
        except:
            pass
        return nodes

menu_pool.register_modifier(GenerateReverseIdModifier)
