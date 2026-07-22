My Estate
=========

``my_estate`` is a training module for managing real estate properties,
offers, tags, types, portal access, website pages, reports, and cancellation
workflow examples.

Repository structure
====================

The Git repository root is the parent workspace. This module is only one custom
addon inside the Odoo training project.

::

    VDX-intern/
    ├── .git/                  # Git metadata directory
    ├── .gitignore             # Repository ignore rules
    ├── odoo-traning/
    │   ├── .pylint
    │   ├── odools.toml
    │   ├── odoo-19/           # Odoo source code
    │   └── custom_addons/
    │       ├── intern_sales/
    │       └── my_estate/     # This module
    └── ...

Module directory structure
==========================

::

    my_estate/
    ├── __init__.py
    ├── __manifest__.py
    ├── controllers/
    │   └── property.py
    ├── data/
    │   ├── estate_property_tag_data.xml
    │   └── estate_property_type_data.xml
    ├── i18n/
    │   └── vi.po
    ├── models/
    │   ├── estate_property.py
    │   ├── estate_property_offer.py
    │   ├── estate_property_tag.py
    │   └── estate_property_type.py
    ├── report/
    │   └── estate_property_report.xml
    ├── security/
    │   ├── ir.model.access.csv
    │   └── security.xml
    ├── tests/
    │   └── test_security.py
    ├── views/
    │   ├── estate_menus.xml
    │   ├── estate_property_offer_views.xml
    │   ├── estate_property_tag_views.xml
    │   ├── estate_property_type_views.xml
    │   ├── estate_property_views.xml
    │   └── estate_website_templates.xml
    └── wizard/
        ├── estate_property_cancel_wizard.py
        └── estate_property_cancel_wizard_views.xml

Main folders
============

``models/``
    Business models for properties, offers, property tags, and property types.

``views/``
    Backend menu, action, form, list, search, and website templates.

``wizard/``
    Transient models and views for user-assisted workflows, such as cancelling
    a property with a reason.

``security/``
    Access control lists, security groups, and record rules.

``data/``
    Demo or initial records loaded by the module.

``controllers/``
    Website and HTTP route logic.

``report/``
    Report templates and report actions.

``tests/``
    Automated tests for module behavior and security rules.
