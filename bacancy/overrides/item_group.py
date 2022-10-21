import frappe
from frappe import _

from frappe.utils.nestedset import get_root_of, get_descendants_of


def onload(doc, method=None):
    doc.set_onload("root_item_group", get_root_item_group())


def validate(doc, method=None):
    root_item_group = get_root_item_group()

    if (
        frappe.flags.in_install
        or frappe.flags.in_setup_wizard
        or doc.name == root_item_group
    ):
        return

    if not doc.parent_item_group:
        frappe.throw("Parent Item Group is required", frappe.MandatoryError)

    is_category = doc.parent_item_group == root_item_group

    if is_category:
        doc.is_group = 1

        if not doc.pch_sc_item_series:
            frappe.throw("Subcategory Item Series is required", frappe.MandatoryError)

    elif doc.has_value_changed("parent_item_group"):
        doc.pch_sc_item_series = frappe.db.get_value(
            "Item Group",
            doc.parent_item_group,
            "pch_sc_item_series",
        )

    old_doc = doc.get_doc_before_save()
    old_value = old_doc.get("pch_sc_item_series") if old_doc else None
    current_value = doc.pch_sc_item_series

    if old_value and old_value != current_value:
        frappe.throw(
            "Subcategory Item Series cannot be changed from {0} to {1}".format(old_value, current_value)
        )

    if not old_value and is_category:
        update_naming_series(current_value)
        update_descendant_item_groups(doc)


def update_naming_series(item_series):
    naming_series = frappe.get_doc("Naming Series")
    series_list = naming_series.get_options("Item").split("\n")

    if item_series in series_list:
        frappe.throw("Item Series {0} already exists".format(item_series))

    series_list.append(item_series)
    naming_series.set_series_for("Item", series_list)


def update_descendant_item_groups(doc):
    "Helper function to update all descendants when first set."

    if doc.is_new():
        return

    item_groups = get_descendants_of("Item Group", doc.name)
    if not item_groups:
        return

    ItemGroup = frappe.qb.DocType("Item Group")
    (
        frappe.qb.update(ItemGroup)
        .set(ItemGroup.pch_sc_item_series, doc.pch_sc_item_series)
        .where(ItemGroup.name.isin(item_groups))
        .run()
    )


########################################################################################
### Utility Functions
########################################################################################

def get_root_item_group():
    root_item_group = getattr(frappe.local, "root_item_group", None)
    if not root_item_group:
        root_item_group = get_root_of("Item Group") or _("All Item Groups")
        frappe.local.root_item_group = root_item_group

    return root_item_group
