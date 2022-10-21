frappe.ui.form.on("Item Group", {
    parent_item_group(frm) {
        if (!frm.is_new()) return;

        if (is_category(frm)) {
            frm.set_value("is_group", 1);
            return;
        }

        frappe.db.get_value(
            "Item Group",
            frm.doc.parent_item_group,
            "pch_sc_item_series",
            (r) => frm.set_value("pch_sc_item_series", r.pch_sc_item_series),
        );
    }
});

function is_category(frm) {
    const parent_item_group = frm.doc.parent_item_group;
    return parent_item_group && is_root(frm, parent_item_group);
}

function is_root(frm, item_group) {
    if (!item_group) {
        item_group = frm.doc.name;
    };

    return item_group === frm.doc.__onload?.root_item_group;
}
