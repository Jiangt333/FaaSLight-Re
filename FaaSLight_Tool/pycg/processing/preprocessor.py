#
# Copyright (c) 2020 Vitalis Salis.
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
import ast
import os
import importlib

from machinery.definitions import DefinitionManager, Definition
import utils
from processing.base import ProcessingBase

# 内部继承了ProcessingBase的类，以及里面的方法，一般是super表示
class PreProcessor(ProcessingBase):
    def __init__(self, filename, modname,
            import_manager, scope_manager, def_manager, class_manager,
            module_manager, modules_analyzed=None):
        print('preprocessor init----{}'.format(filename))
        if filename.endswith('.so'):
            # print('init encouter so file')
            self.import_manager = None
            self.modules_analyzed = set()
            return

        super().__init__(filename, modname, modules_analyzed)

        

        self.modname = modname
        self.mod_dir = "/".join(self.filename.split("/")[:-1])

        self.import_manager = import_manager
        self.scope_manager = scope_manager
        self.def_manager = def_manager
        self.class_manager = class_manager
        self.module_manager = module_manager

    # jt添加
    def _get_fun_defaults(self, node):
        defaults = {}
        
        # 处理位置参数默认值
        if node.args.defaults and node.args.args:
            # 确保不越界
            start = max(0, len(node.args.args) - len(node.args.defaults))
            for i, d in enumerate(node.args.defaults):
                if not d:
                    continue
                self.visit(d)
                # 计算正确的参数索引
                arg_index = start + i
                if arg_index < len(node.args.args):
                    defaults[node.args.args[arg_index].arg] = self.decode_node(d)
        
        # 处理关键字参数默认值
        if node.args.kw_defaults and node.args.kwonlyargs:
            start = max(0, len(node.args.kwonlyargs) - len(node.args.kw_defaults))
            for i, d in enumerate(node.args.kw_defaults):
                if not d:
                    continue
                self.visit(d)
                arg_index = start + i
                if arg_index < len(node.args.kwonlyargs):
                    defaults[node.args.kwonlyargs[arg_index].arg] = self.decode_node(d)
        
        return defaults

    # def _get_fun_defaults(self, node):
    #     defaults = {}
    #     start = len(node.args.args) - len(node.args.defaults)
    #     for cnt, d in enumerate(node.args.defaults, start=start):
    #         if not d:
    #             continue

    #         self.visit(d)
    #         defaults[node.args.args[cnt].arg] = self.decode_node(d)

    #     start = len(node.args.kwonlyargs) - len(node.args.kw_defaults)
    #     for cnt, d in enumerate(node.args.kw_defaults, start=start):
    #         if not d:
    #             continue
    #         self.visit(d)
    #         defaults[node.args.kwonlyargs[cnt].arg] = self.decode_node(d)

    #     return defaults

    def analyze_submodule(self, modname):
        super().analyze_submodule(PreProcessor, modname,
            self.import_manager, self.scope_manager, self.def_manager, self.class_manager,
            self.module_manager, modules_analyzed=self.get_modules_analyzed())

    # 在Python中，每个文件都被视为一个模块，模块是代码组织的基本单元。visit_Module 方法是 PreProcessor 类中的一个方法，用于处理模块级别的代码。
    def visit_Module(self, node):
        def iterate_mod_items(items, const):  # 遍历模块中的项（函数/类），创建定义并添加到父作用域
            for item in items:
                # 获取或创建定义
                defi = self.def_manager.get(item)
                if not defi:
                    defi = self.def_manager.create(item, const)

                # # 解析命名空间：将定义的名称拆分成多个部分，并获取最后一个部分作为名称，其余部分作为父命名空间
                splitted = item.split(".")
                name = splitted[-1]
                parentns = ".".join(splitted[:-1])
                # 将定义添加到父作用域
                self.scope_manager.get_scope(parentns).add_def(name, defi)
        # 设置当前模块的导入管理器，告诉导入管理器当前正在处理哪个模块，用于后续的导入管理
        self.import_manager.set_current_mod(self.modname, self.filename)
        # 创建模块管理器条目，在 module_manager 中创建一个模块记录，用于后续的模块管理
        mod = self.module_manager.create(self.modname, self.filename)

        # 获取模块的开始和结束行号，用于后续的模块管理
        first = 1
        last = len(self.contents.splitlines())
        if last == 0:
            first = 0
        mod.add_method(self.modname, first, last)  # 这里把整个模块当作一个"方法"来记录

        # 初始化模块作用域。获取根作用域，如果根作用域不存在，则创建根作用域
        root_sc = self.scope_manager.get_scope(self.modname)
        if not root_sc:
            # initialize module scopes
            # 1. 处理模块，生成符号表并遍历进行process，在其中调用create_scope添加到作用域，并生成一个包含函数和类名的字典返回
            items = self.scope_manager.handle_module(self.modname,
                self.filename, self.contents)

            # 2. 获取刚创建的作用域
            root_sc = self.scope_manager.get_scope(self.modname)
            # 3. 创建模块根定义。获取模块根定义，如果模块根定义不存在，则创建模块根定义
            root_defi = self.def_manager.get(self.modname)
            if not root_defi:
                root_defi = self.def_manager.create(self.modname, utils.constants.MOD_DEF)
            # 4. 将模块定义添加到自身作用域
            root_sc.add_def(self.modname.split(".")[-1], root_defi)

            # create function and class defs and add them to their scope
            # we do this here, because scope_manager doesn't have an
            # interface with def_manager, and we want function definitions
            # to have the correct points_to set
            # 5. 为模块中的函数和类创建定义并添加到作用域
            iterate_mod_items(items["functions"], utils.constants.FUN_DEF)
            iterate_mod_items(items["classes"], utils.constants.CLS_DEF)

        defi = self.def_manager.get(self.modname)
        if not defi:
            defi = self.def_manager.create(self.modname, utils.constants.MOD_DEF)

        super().visit_Module(node)

    # 用于处理Python中的import语句和from ... import ...语句
    def visit_Import(self, node, prefix='', level=0):
        """
        For imports of the form
            `from something import anything`
        prefix is set to "something".
        For imports of the form
            `from .relative import anything`
        level is set to a number indicating the number
        of parent directories (e.g. in this case level=1)
        """
        # 构建完整的导入源名称
        def handle_src_name(name):
            # Get the module name and prepend prefix if necessary
            src_name = name
            if prefix:
                src_name = prefix + "." + src_name
            return src_name

        # def handle_scopes(imp_name, tgt_name, modname):
        #     print('sssshhhhh')
        #     def create_def(scope, name, imported_def):
        #         print('ssss')
        #         if not name in scope.get_defs():
        #             def_ns = utils.join_ns(scope.get_ns(), name)
        #             defi = self.def_manager.get(def_ns)
        #             if not defi:
        #                 defi = self.def_manager.assign(def_ns, imported_def)
        #             defi.get_name_pointer().add(imported_def.get_ns())
        #             current_scope.add_def(name, defi)

        #     current_scope = self.scope_manager.get_scope(self.current_ns)
        #     imported_scope = self.scope_manager.get_scope(modname)
        #     if tgt_name == "*":
        #         for name, defi in imported_scope.get_defs().items():
        #             create_def(current_scope, name, defi)
        #             current_scope.get_def(name).get_name_pointer().add(defi.get_ns())
        #     else:
        #         # if it exists in the imported scope then copy it
        #         defi = imported_scope.get_def(imp_name)
        #         if not defi:
        #             # maybe its a full namespace
        #             defi = self.def_manager.get(imp_name)

        #         if defi:
        #             create_def(current_scope, tgt_name, defi)
        #             current_scope.get_def(tgt_name).get_name_pointer().add(defi.get_ns())


        def handle_scopes(imp_name, tgt_name, modname):
            # print('sssshhhhh')
            # 创建一个指向import定义的新定义。如果定义不存在，则创建定义，并添加到作用域
            def create_def(scope, name, imported_def):
                # print('ssss')
                if not name in scope.get_defs():
                    def_ns = utils.join_ns(scope.get_ns(), name)   # 当前作用域下的完整命名空间（当前作用域+名称）
                    # 获取或创建一个定义，指向import的定义
                    defi = self.def_manager.get(def_ns)
                    if not defi:
                        defi = self.def_manager.assign(def_ns, imported_def)
                    defi.get_name_pointer().add(imported_def.get_ns())
                    current_scope.add_def(name, defi)

            current_scope = self.scope_manager.get_scope(self.current_ns)
            imported_scope = self.scope_manager.get_scope(modname)
            if tgt_name == "*":
                if imported_scope:
                    for name, defi in imported_scope.get_defs().items():
                        create_def(current_scope, name, defi)
                        current_scope.get_def(name).get_name_pointer().add(defi.get_ns())
            else:
                # if it exists in the imported scope then copy it
                if imported_scope:
                    defi = imported_scope.get_def(imp_name)
                    if not defi:
                        # maybe its a full namespace
                        defi = self.def_manager.get(imp_name)

                    if defi:
                        create_def(current_scope, tgt_name, defi)
                        current_scope.get_def(tgt_name).get_name_pointer().add(defi.get_ns())




        def add_external_def(name, target):
            # add an external def for the name
            defi = self.def_manager.get(name)
            if not defi:
                defi = self.def_manager.create(name, utils.constants.EXT_DEF)
            scope = self.scope_manager.get_scope(self.current_ns)
            if target != "*":
                # add a def for the target that points to the name
                tgt_ns = utils.join_ns(scope.get_ns(), target)
                tgt_defi = self.def_manager.get(tgt_ns)
                if not tgt_defi:
                    tgt_defi = self.def_manager.create(tgt_ns, utils.constants.EXT_DEF)
                tgt_defi.get_name_pointer().add(defi.get_ns())
                scope.add_def(target, tgt_defi)

        for import_item in node.names:
            src_name = handle_src_name(import_item.name)
            tgt_name = import_item.asname if import_item.asname else import_item.name
            imported_name = self.import_manager.handle_import(src_name, level)

            if not imported_name:
                add_external_def(src_name, tgt_name)
                continue

            fname = self.import_manager.get_filepath(imported_name)

            # print(f"DEBUG visit_Import: Processing import in module {self.modname}, imported_name={imported_name}, fname={fname}")
            # print(f"DEBUG visit_Import: current_ns = {self.current_ns}")
            # print(f"DEBUG visit_Import: modules_analyzed = {self.modules_analyzed}")
            # print(f"DEBUG visit_Import: import_manager.get_mod_dir() = {self.import_manager.get_mod_dir()}")
            # if fname:
            #     print(f"DEBUG visit_Import: self.import_manager.get_mod_dir() in fname = {self.import_manager.get_mod_dir() in fname}, not modname in self.modules_analyzed={not imported_name in self.modules_analyzed}")
            # else:
            #     print(f"DEBUG visit_Import: fname is None, not imported_name in self.modules_analyzed={not imported_name in self.modules_analyzed}")

            if not fname:
                add_external_def(src_name, tgt_name)
                continue
            # only analyze modules under the current directory
            if self.import_manager.get_mod_dir() in fname:
                if not imported_name in self.modules_analyzed:
                    self.analyze_submodule(imported_name)
                handle_scopes(import_item.name, tgt_name, imported_name)
            else:
                add_external_def(src_name, tgt_name)

        # handle all modules that were not analyzed
        for modname in self.import_manager.get_imports(self.modname):
            fname = self.import_manager.get_filepath(modname)
            # print('=================')
            # print(f"DEBUG visit_Import 2: Processing import in module {self.modname}, modname={modname}, fname={fname}")
            # print(f"DEBUG visit_Import 2: current_ns = {self.current_ns}")
            # print(f"DEBUG visit_Import 2: modules_analyzed = {self.modules_analyzed}")
            # print(f"DEBUG visit_Import 2: import_manager.get_mod_dir() = {self.import_manager.get_mod_dir()}")
            # print(f"DEBUG visit_Import 2: self.import_manager.get_mod_dir() in fname = {(self.import_manager.get_mod_dir() in fname) if fname else 'N/A (fname is None)'}, not modname in self.modules_analyzed={not modname in self.modules_analyzed}")

            if not fname:
                continue
            # only analyze modules under the current directory
            if self.import_manager.get_mod_dir() in fname and \
                not modname in self.modules_analyzed:
                    self.analyze_submodule(modname)


    def visit_ImportFrom(self, node):
        self.visit_Import(node, prefix=node.module, level=node.level)

    def _get_last_line(self, node):
        lines = sorted(list(ast.walk(node)), key=lambda x: x.lineno if hasattr(x, "lineno") else 0, reverse=True)
        if not lines:
            return node.lineno

        last = getattr(lines[0], "lineno", node.lineno)
        if last < node.lineno:
            return node.lineno

        return last

    def _handle_function_def(self, node, fn_name):
        current_def = self.def_manager.get(self.current_ns)

        defaults = self._get_fun_defaults(node)

        fn_def = self.def_manager.handle_function_def(self.current_ns, fn_name)

        mod = self.module_manager.get(self.modname)
        if not mod:
            mod = self.module_manager.create(self.modname, self.filename)
        mod.add_method(fn_def.get_ns(), node.lineno, self._get_last_line(node))

        defs_to_create = []
        name_pointer = fn_def.get_name_pointer()

        # TODO: static methods can be created using the staticmethod() function too
        is_static_method = False
        if hasattr(node, "decorator_list"):
            for decorator in node.decorator_list:
                if isinstance(decorator, ast.Name) and decorator.id == utils.constants.STATIC_METHOD:
                    is_static_method = True

        if current_def.get_type() == utils.constants.CLS_DEF and not is_static_method and node.args.args:
            arg_ns = utils.join_ns(fn_def.get_ns(), node.args.args[0].arg)
            arg_def = self.def_manager.get(arg_ns)
            if not arg_def:
                arg_def = self.def_manager.create(arg_ns, utils.constants.NAME_DEF)
            arg_def.get_name_pointer().add(current_def.get_ns())

            self.scope_manager.handle_assign(fn_def.get_ns(), arg_def.get_name(), arg_def)
            node.args.args = node.args.args[1:]

        for pos, arg in enumerate(node.args.args):
            arg_ns = utils.join_ns(fn_def.get_ns(), arg.arg)
            name_pointer.add_pos_arg(pos, arg.arg, arg_ns)
            defs_to_create.append(arg_ns)

        for arg in node.args.kwonlyargs:
            arg_ns = utils.join_ns(fn_def.get_ns(), arg.arg)
            # TODO: add_name_arg function
            name_pointer.add_name_arg(arg.arg, arg_ns)
            defs_to_create.append(arg_ns)

        # TODO: Add support for kwargs and varargs
        #if node.args.kwarg:
        #    pass
        #if node.args.vararg:
        #    pass

        for arg_ns in defs_to_create:
            arg_def = self.def_manager.get(arg_ns)
            if not arg_def:
                arg_def = self.def_manager.create(arg_ns, utils.constants.NAME_DEF)

            self.scope_manager.handle_assign(fn_def.get_ns(), arg_def.get_name(), arg_def)

            # has a default
            arg_name = arg_ns.split(".")[-1]
            if defaults.get(arg_name, None):
                for default in defaults[arg_name]:
                    if isinstance(default, Definition):
                        arg_def.get_name_pointer().add(default.get_ns())
                        if default.is_function_def():
                            arg_def.get_name_pointer().add(default.get_ns())
                        else:
                            arg_def.merge(default)
                    else:
                        arg_def.get_lit_pointer().add(default)
        return fn_def

    def visit_FunctionDef(self, node):
        fn_def = self._handle_function_def(node, node.name)

        super().visit_FunctionDef(node)

    def visit_For(self, node):
        # just create the definition for target
        if isinstance(node.target, ast.Name):
            target_ns = utils.join_ns(self.current_ns, node.target.id)
            if not self.def_manager.get(target_ns):
                defi = self.def_manager.create(target_ns, utils.constants.NAME_DEF)
                self.scope_manager.get_scope(self.current_ns).add_def(node.target.id, defi)
        super().visit_For(node)

    def visit_Assign(self, node):
        self._visit_assign(node.value, node.targets)

    def visit_Return(self, node):
        self._visit_return(node)

    def visit_Yield(self, node):
        self._visit_return(node)

    def visit_Call(self, node):
        self.visit(node.func)
        # if it is not a name there's nothing we can do here
        # ModuleVisitor will be able to resolve those calls
        # since it'll have the name tracking information
        if not isinstance(node.func, ast.Name):
            return

        fullns = utils.join_ns(self.current_ns, node.func.id)

        defi = self.scope_manager.get_def(self.current_ns, node.func.id)
        if not defi:
            return

        if defi.get_type() == utils.constants.CLS_DEF:
            defi = self.def_manager.get(utils.join_ns(defi.get_ns(), utils.constants.CLS_INIT))
            if not defi:
                return

        self.iterate_call_args(defi, node)

    def visit_Lambda(self, node):
        # The name of a lambda is defined by the counter of the current scope
        current_scope = self.scope_manager.get_scope(self.current_ns)
        lambda_counter = current_scope.inc_lambda_counter()
        lambda_name = utils.get_lambda_name(lambda_counter)
        lambda_full_ns = utils.join_ns(self.current_ns, lambda_name)

        # create a scope for the lambda
        self.scope_manager.create_scope(lambda_full_ns, current_scope)
        lambda_def = self._handle_function_def(node, lambda_name)
        # add it to the current scope
        current_scope.add_def(lambda_name, lambda_def)

        super().visit_Lambda(node, lambda_name)

    def visit_ClassDef(self, node):
        # create a definition for the class (node.name)
        cls_def = self.def_manager.handle_class_def(self.current_ns, node.name)

        mod = self.module_manager.get(self.modname)
        if not mod:
            mod = self.module_manager.create(self.modname, self.filename)
        mod.add_method(cls_def.get_ns(), node.lineno, self._get_last_line(node))

        # iterate bases to compute MRO for the class
        cls = self.class_manager.get(cls_def.get_ns())
        if not cls:
            cls = self.class_manager.create(cls_def.get_ns(), self.modname)

        super().visit_ClassDef(node)

    def analyze(self):
        # if not self.import_manager.get_node(self.modname):
        #     if self.filename.endswith('.so'):
        #         print('encouter so file')
        #     else:
        #         self.import_manager.create_node(self.modname)
        #         self.import_manager.set_filepath(self.modname, self.filename)
        #         print('preprocessing analyze- function-----{}'.format(self.filename))
        #         self.visit(ast.parse(self.contents, self.filename))

        if not self.import_manager:
            # print('analyze not handler')
            return

        if not self.import_manager.get_node(self.modname):
            self.import_manager.create_node(self.modname)
            self.import_manager.set_filepath(self.modname, self.filename)
            # print('preprocessing analyze- function-----{}'.format(self.filename))

        # 解析文件内容为AST，并开始遍历，会根据节点的类型调用相应的visit_方法
        # print('visit file')
        self.visit(ast.parse(self.contents, self.filename))
