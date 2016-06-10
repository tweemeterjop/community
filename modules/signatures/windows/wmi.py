# Copyright (C) 2010-2015 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import re

from lib.cuckoo.common.abstracts import Signature

class HasWMI(Signature):
    name = "has_wmi"
    description = "Executes one or more WMI queries"
    severity = 2
    categories = ["wmi"]
    authors = ["Cuckoo Technologies"]
    minimum = "2.0"

    blacklist = "(AntivirusProduct|FirewallProduct)"

    def on_complete(self):
        for query in self.get_wmi_queries():
            self.mark_ioc("wmi", query)

            if re.search(self.blacklist, query, re.I):
                self.severity = 3

        return self.has_marks()

class Win32ProcessCreate(Signature):
    name = "win32_process_create"
    description = "Uses WMI to create a new process"
    severity = 4
    categories = ["wmi"]
    authors = ["Cuckoo Technologies"]
    minimum = "2.0"

    filter_apinames = [
        "IWbemServices_ExecMethod",
        "IWbemServices_ExecMethodAsync",
    ]

    def on_call(self, call, process):
        if call["arguments"]["class"] == "Win32_Process" and \
                call["arguments"]["method"] == "Create":
            self.mark_call()
            return True
