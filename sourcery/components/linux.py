# sourcery-builder linux component.

# Copyright 2018-2019 Mentor Graphics Corporation.

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

"""sourcery-builder linux component."""

from sourcery.buildtask import BuildTask
import sourcery.component
from sourcery.fstree import FSTreeMove

__all__ = ['Component']


# This covers all architectures that, as of November 2018, have
# support in both the Linux kernel and GNU config.sub, but does not
# try to cover all the variant legacy aliases for some architectures
# that are also supported by config.sub.
_LINUX_ARCH_MAP = {'aarch64': 'arm64',
                   'alpha': 'alpha',
                   'arc': 'arc',
                   'arm': 'arm',
                   'c6x': 'c6x',
                   'csky': 'csky',
                   'h8300': 'h8300',
                   'hexagon': 'hexagon',
                   'hppa': 'parisc',
                   'i486': 'x86',
                   'i586': 'x86',
                   'i686': 'x86',
                   'i786': 'x86',
                   'ia64': 'ia64',
                   'm68k': 'm68k',
                   'microblaze': 'microblaze',
                   'mips': 'mips',
                   'nds32': 'nds32',
                   'nios2': 'nios2',
                   'or1k': 'openrisc',
                   'powerpc': 'powerpc',
                   'riscv': 'riscv',
                   's390': 's390',
                   'sh': 'sh',
                   'sparc': 'sparc',
                   'tic6x': 'c6x',
                   'x86_64': 'x86',
                   'xtensa': 'xtensa'}

_INST_NAME = 'linux-headers'


def _contribute_headers_tree(cfg, host, host_group, is_build):
    """Contribute the installed headers to all required install trees."""
    host_b = host.build_cfg
    build = cfg.build.get().build_cfg
    tree = cfg.install_tree_fstree(build, _INST_NAME)
    # headers_install puts headers in an include/ subdirectory of the
    # given path.
    tree = FSTreeMove(tree, '%s/usr' % cfg.sysroot_rel.get())
    if is_build:
        host_group.contribute_implicit_install(host_b, 'toolchain-1-before',
                                               tree)
        host_group.contribute_implicit_install(host_b, 'toolchain-1', tree)
        host_group.contribute_implicit_install(host_b, 'toolchain-2-before',
                                               tree)
        host_group.contribute_implicit_install(host_b, 'toolchain-2', tree)
    host_group.contribute_package(host, tree)


class Component(sourcery.component.Component):
    """sourcery-builder linux component implementation."""

    @staticmethod
    def add_release_config_vars(group):
        group.source_type.set_implicit('open')

    @staticmethod
    def add_build_tasks_for_first_host(cfg, host, component, host_group):
        host_b = host.build_cfg
        srcdir = component.vars.srcdir.get()
        objdir = cfg.objdir_path(host_b, 'linux')
        instdir = cfg.install_tree_path(host_b, _INST_NAME)
        task = BuildTask(cfg, host_group, 'linux-headers')
        task.provide_install(host_b, _INST_NAME)
        task.add_empty_dir(objdir)
        task.add_empty_dir(instdir)
        linux_arch = None
        target = cfg.target.get()
        for gnu_arch in _LINUX_ARCH_MAP:
            if target.startswith(gnu_arch):
                linux_arch = _LINUX_ARCH_MAP[gnu_arch]
                break
        if linux_arch is None:
            cfg.context.error('unknown Linux kernel architecture for %s'
                              % target)
        task.add_make(['-C', srcdir, 'O=%s' % objdir, 'ARCH=%s' % linux_arch,
                       'INSTALL_HDR_PATH=%s' % instdir,
                       'headers_install'], objdir)
        _contribute_headers_tree(cfg, host, host_group, True)

    @staticmethod
    def add_build_tasks_for_other_hosts(cfg, host, component, host_group):
        _contribute_headers_tree(cfg, host, host_group, False)
