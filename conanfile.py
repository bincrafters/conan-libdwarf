# -*- coding: utf-8 -*-
from conans import ConanFile, CMake, tools
import os


class LibdwarfConan(ConanFile):
    name = "libdwarf"
    version = "20190505"
    description = "A library and a set of command-line tools for reading and writing DWARF2"
    topics = ("conan", "libdwarf", "dwarf2", "debugging", "dwarf")
    url = "https://github.com/bincrafters/conan-libdwarf"
    homepage = "https://www.prevanders.net/dwarf.html"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "LGPL-2.1"
    exports = ["LICENSE.md"]
    exports_sources = ["CMakeLists.txt", "0001-install.patch"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}
    requires = ("libelf/0.8.13@bincrafters/stable", "zlib/1.2.11@conan/stable")

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_folder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        del self.settings.compiler.libcxx

    def source(self):
        source_url = "https://sourceforge.net/code-snapshots/git/l/li/libdwarf/code.git"
        commit = "c6660d75c2affc3e2f1231ad55942734060d98e6"
        sha256 = "7f0bc94c82bb3130f4a3d20e14ccb45656ad54d412c8b2edfc3d33981803a72d"
        extracted_dir = self.name + "-code-" + commit
        tools.get("{}/{}.zip".format(source_url, extracted_dir), sha256=sha256)
        os.rename(extracted_dir, self._source_subfolder)

    def _configure_cmake(self):
        cmake = CMake(self)
        cmake.definitions["nonshared"] = not self.options.shared
        cmake.definitions["shared"] = self.options.shared
        cmake.configure(build_folder=self._build_subfolder)
        return cmake

    def build(self):
        tools.patch(base_path=self._source_subfolder, patch_file="0001-install.patch")
        cmake = self._configure_cmake()
        cmake.build()

    def package(self):
        self.copy(pattern="COPYING", dst="licenses", src=os.path.join(self._source_subfolder, "libdwarf"))
        cmake = self._configure_cmake()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = tools.collect_libs(self)
