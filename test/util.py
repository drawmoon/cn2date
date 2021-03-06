from typing import Union


def get_node_value(tree, data) -> Union[str, None]:
    nodes = list(tree.find_data(data))

    if len(nodes) == 0:
        return None

    val = "".join([c.value for c in nodes[0].children])
    print("output", val)

    return val
