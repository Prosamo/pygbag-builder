import ast
import astor
import os

class AsyncifyWhileFunctions(ast.NodeTransformer):
    def __init__(self):
        self.async_functions = set()
        self.import_asyncio = False
        self.main_transformed = False
    # If the function contains while loop, insert await asyncio.sleep(0) at the top of loop and remake it into async function.
    def visit_FunctionDef(self, node):
        has_while = any(isinstance(subnode, ast.While) for subnode in ast.walk(node))
        if has_while:
            # remake into async function
            self.async_functions.add(node.name)
            node = ast.AsyncFunctionDef(
                name=node.name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list,
                returns=node.returns,
                type_comment=node.type_comment
            )
            # insert await asyncio.sleep(0)
            for subnode in ast.walk(node):
                if isinstance(subnode, ast.While):
                    # make sentence for insert
                    sleep_call = ast.Await(
                        ast.Call(
                            func=ast.Attribute(value=ast.Name(id='asyncio', ctx=ast.Load()), attr='sleep', ctx=ast.Load()),
                            args=[ast.Constant(value=0)],
                            keywords=[]
                        )
                    )
                    # insert at the top of while loop
                    subnode.body.insert(0, ast.Expr(value=sleep_call))
        return node

    def visit_Call(self, node):
        if isinstance(node.func, ast.Name):
            # The special process for main function. (Because we need to call it like 'asyncio.run(main())')
            if node.func.id == 'main' and not self.main_transformed:
                self.main_transformed = True
                return ast.Call(
                    func=ast.Attribute(value=ast.Name(id='asyncio', ctx=ast.Load()), attr='run', ctx=ast.Load()),
                    args=[node],
                    keywords=[]
                )
            elif node.func.id in self.async_functions:
                if not isinstance(node, ast.Await):
                    return ast.Await(value=node)
        return node
    # Check if asyncio is imported
    def visit_Import(self, node):
        for alias in node.names:
            if alias.name == 'asyncio':
                self.import_asyncio = True
        return node
    # insert 'import asyncio' if it is needed. 
    def visit_Module(self, node):
        self.generic_visit(node)
        if self.async_functions and not self.import_asyncio:
            import_node = ast.Import(names=[ast.alias(name='asyncio', asname=None)])
            node.body.insert(0, import_node)
        return node
# make the code modifide
def transform_code(source_code):
    tree = ast.parse(source_code)
    transformer = AsyncifyWhileFunctions()
    new_tree = transformer.visit(tree)
    
    #while True:
    #    async_functions_before = set(transformer.async_functions)
    #    new_tree = transformer.visit(new_tree)
    #    if async_functions_before == transformer.async_functions:
    #        break
    
    new_code = astor.to_source(new_tree)
    return new_code

#get '.py' files from current directory and make those files modified
def process_files_in_directory(directory):
    output_directory = os.path.join(directory, 'pygbag_builder_build')
    os.makedirs(output_directory, exist_ok=True)
    
    excluded_files = {'main_flow.py', 'make_dir.py', 'insert_sleep.py', 'insert_await.py', 'setup.py'}
    file_paths = [os.path.join(directory, filename) for filename in os.listdir(directory) if filename.endswith('.py') and filename not in excluded_files]
    
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            source_code = file.read()
        
        transformed_code = transform_code(source_code)
        
        output_filepath = os.path.join(output_directory, os.path.basename(file_path))
        with open(output_filepath, 'w', encoding='utf-8') as file:
            file.write(transformed_code)

if __name__ == "__main__":
    current_directory = os.getcwd()
    process_files_in_directory(current_directory)
