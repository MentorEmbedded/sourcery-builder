# Base class for sourcery-builder components.

# Copyright 2018 Mentor Graphics Corporation.

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as
# published by the Free Software Foundation; either version 2.1 of the
# License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public
# License along with this program; if not, see
# <https://www.gnu.org/licenses/>.

"""Base class for sourcery-builder components."""

__all__ = ['Component']


class Component:
    """Base class from which each component's class inherits."""

    @staticmethod
    def add_release_config_vars(group):
        """Set up release config variables for this component.

        Add any release config variables specific to this component.
        Override any variables that are defined for all components but
        where the default is inappropriate to this one.

        """

    files_to_touch = []
    """Files to touch after checkout.

    The names are interpreted as Python glob patterns (recursive, so
    '**' can be used to find files of a given name in any
    subdirectory).  Files are only touched if they exist.  Files are
    touched at the same time or in the order given.

    """

    @staticmethod
    def postcheckout(context, component):
        """Touch files after checkout.

        This is passed the ComponentInConfig object.  This hook is for
        the case where the component sources provide their own script
        to touch files to put timestamps in the right order.  It must
        not do anything other than changing timestamps of files.
        files_to_touch is used first, then the postcheckout hook is
        run (but normally there is no use for setting both).

        """

    @staticmethod
    def add_build_tasks_for_host(cfg, host, component, host_group):
        """Add any host-specific build tasks associated with this component.

        Such tasks should be added with 'host_group' (a group
        containing tasks to be run in parallel) as their parent; 'cfg'
        is the release config and 'host' is the corresponding PkgHost
        object.  'component' is the ComponentInConfig object.

        """

    @staticmethod
    def add_build_tasks_for_first_host(cfg, host, component, host_group):
        """Add any host-specific build tasks associated with this component
        that should run for the first host only.

        Such tasks should be added with 'host_group' (a group
        containing tasks to be run in parallel) as their parent; 'cfg'
        is the release config and 'host' is the corresponding PkgHost
        object.  'component' is the ComponentInConfig object.

        """

    @staticmethod
    def add_build_tasks_for_other_hosts(cfg, host, component, host_group):
        """Add any host-specific build tasks associated with this component
        that should run for host other than the first host only.

        Such tasks should be added with 'host_group' (a group
        containing tasks to be run in parallel) as their parent; 'cfg'
        is the release config and 'host' is the corresponding PkgHost
        object.  'component' is the ComponentInConfig object.

        """

    @staticmethod
    def configure_opts(cfg, host):  # pylint: disable=unused-argument
        """Return component-specific configure options.

        These go after standard configure options and before standard
        configure variables.  This function is a convenience hook for
        components whose add_build_tasks_for_host functions use common
        support for configure-based components, and is not relevant
        for components built in other ways whose
        add_build_tasks_for_host functions do not make use, directly
        or indirectly, of this function.  The host passed is the
        BuildCfg object.

        """
        return []
