from bacancy.overrides.item_group import get_root_item_group


def set_bootinfo(bootinfo):
    bootinfo["root_item_group"] = get_root_item_group()
