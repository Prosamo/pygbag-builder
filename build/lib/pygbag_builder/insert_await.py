import ast
import os
import re
import astor

def find_all_async_functions(directory):
    async_functions = []

    # Iterate over all '.py' files in the target directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                # Parse the source code and find async functions
                tree = ast.parse(source_code)
                for node in ast.walk(tree):
                    if isinstance(node, ast.AsyncFunctionDef):
                        async_functions.append(node.name)
                    elif isinstance(node, ast.FunctionDef):
                        # Check if the function is a method of a class
                        if any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                            async_functions.append(node.name)
    
    return async_functions

def replace_function_calls(directory, async_functions):
    # Create a regex pattern to match function calls that are not already awaited, defined, or preceded by asyncio.run or a dot
    pattern = re.compile(r'(?<!def\s)(?<!await\s)(?<!\.)(?<!asyncio\.run\()(?:' + '|'.join(async_functions) + r')\s*\(')
    method_pattern = re.compile(r'(?<!await\s)(\b(?:\w+\.)+\b(?:' + '|'.join(async_functions) + r'))\s*\(')

    # Iterate over all '.py' files in the target directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                # Replace standalone function calls with await function calls
                new_source_code = re.sub(pattern, lambda match: 'await ' + match.group(0), source_code)
                # Replace method calls with await method calls
                new_source_code = re.sub(method_pattern, lambda match: 'await ' + match.group(1) + '(', new_source_code)

                # Remove duplicate 'await' if present
                new_source_code = re.sub(r'await\s+await\s+', 'await ', new_source_code)

                # Write the updated code back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_source_code)

class AsyncFunctionTransformer(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Check if the function contains an await expression
        has_await = any(isinstance(subnode, ast.Await) for subnode in ast.walk(node))
        if has_await:
            # Convert the function to async
            new_node = ast.AsyncFunctionDef(
                name=node.name,
                args=node.args,
                body=node.body,
                decorator_list=node.decorator_list,
                returns=node.returns,
                type_comment=node.type_comment
            )
            return new_node
        return node

def convert_functions_to_async(directory):
    # Iterate over all .py files in the target directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    source_code = f.read()
                
                # Parse the source code and convert functions containing 'await' to async
                tree = ast.parse(source_code)
                transformer = AsyncFunctionTransformer()
                new_tree = transformer.visit(tree)
                
                new_source_code = astor.to_source(new_tree)

                # Write the updated code back to the file
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_source_code)

def process_files_until_no_change(current_dir):
    previous_source_codes = {}
    
    while True:
        current_source_codes = {}

        # Get the path of the directory with the same name as the current directory
        target_dir_path = os.path.join(current_dir, 'pygbag_builder_build')

        # Find all async functions in the target directory
        async_functions = find_all_async_functions(target_dir_path)

        # Replace function calls with await function calls
        replace_function_calls(target_dir_path, async_functions)

        # Convert functions containing 'await' to async
        convert_functions_to_async(target_dir_path)

        # Read all .py files and store their source code
        for root, dirs, files in os.walk(target_dir_path):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r', encoding='utf-8') as f:
                        current_source_codes[file_path] = f.read()

        if current_source_codes == previous_source_codes:
            break
        
        previous_source_codes = current_source_codes

if __name__ == "__main__":
    # Process files until no more changes are detected
    process_files_until_no_change(os.getcwd())

    print("All .py files have been updated.")
