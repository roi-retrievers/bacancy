import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def create_fixtures():
    create_fields()
    create_property_setters()


def create_fields():
    custom_fields = {
        "Item Group": [
            {
                "fieldname": "pch_sc_item_series",
                "label": "Subcategory Item Series",
                "fieldtype": "Data",
                "insert_after": "column_break_5",
                "description": "eg. RES- for RES-00001, CAP- for CAP-00001, etc.",
                "mandatory_depends_on": (
                    "eval: doc.parent_item_group === doc.__onload?.root_item_group"
                ),
                "read_only_depends_on": (
                    "eval: doc.parent_item_group !== doc.__onload?.root_item_group ||"
                    " !doc.__islocal && doc.pch_sc_item_series"
                ),
                "translatable": 0,
            },
        ]
    }

    create_custom_fields(custom_fields)


def create_property_setters():
    property_setters = [
        {
            "doctype": "Item Group",
            "fieldname": "is_group",
            "property": "read_only_depends_on",
            "value": "eval: doc.parent_item_group === doc.__onload?.root_item_group",
        },
        {
            "doctype": "Item Group",
            "fieldname": "parent_item_group",
            "property": "mandatory_depends_on",
            "value": "eval: doc.name !== doc.__onload?.root_item_group",
        },
    ]

    for property_setter in property_setters:
        frappe.make_property_setter(property_setter)
