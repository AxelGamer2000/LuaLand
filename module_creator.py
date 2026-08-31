from sys import argv

import inquirer
from pathlib import Path
import json
import sys

lua_template = Path("lua_template.txt").read_text(encoding="utf-8")

while True:
    modules = [
        path for path in Path("modules").glob("*.lua") if path.is_file()
    ]

    order_file = Path("modules/order.json")
    order_json = json.loads(order_file.read_text(encoding="utf-8"))
    order: list[str] = order_json["order"]
    choices = [module.name for module in modules]

    command = ""

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        print("Commands: create, delete, sync, order, !exit (!!)")
        command = inquirer.text("command")

    if command == "!exit" or command == "!!":
        break
    elif command == "create":
        module_name: str = inquirer.text("Enter a name for the module")
        Path(f"modules/{module_name.replace(" ", "_")}.lua").write_text(lua_template)
    elif command == "delete":
        question: str = inquirer.prompt([
            inquirer.List(
                "delete",
                message="Select a module to delete",
                choices=choices
            )
        ])["delete"]

        for module in modules:
            if module.name == question:
                module.unlink()
                break
    elif command == "sync":
        counter = 0
        temp_order = []

        if len(modules) == 0:
            order_json["order"] = []
            order_file.write_text(json.dumps(order_json, indent=2))
            print(f"empty sync")
        else:
            for module in modules:
                if not str(module) in order:
                    order.append(str(module))
                    counter += 1

            if len(modules) != len(order):
                for content in order:
                    if Path(content) in modules:
                        temp_order.append(content)

                order = temp_order

            order_json["order"] = order
            order_file.write_text(json.dumps(order_json, indent=2))

            print(f"{counter} modules sync")


    elif command == "order":
        while True:
            from_module: Path = None
            from_module_name: str = inquirer.prompt([
                inquirer.List(
                "from",
                    message="Select from a module",
                    choices=choices
                )
            ])["from"]

            to_module: Path = None
            to_module_name: str = inquirer.prompt([
                inquirer.List(
                    "to",
                    message="Select to a module",
                    choices=choices
                )
            ])["to"]

            for module in modules:
                if from_module_name == module.name:
                    from_module = module
                    break

            for module in modules:
                if to_module_name == module.name:
                    to_module = module
                    break

            from_index = order.index(str(from_module))
            to_index = order.index(str(to_module))

            order[from_index], order[to_index] = order[to_index], order[from_index]

            order_json["order"] = order
            order_file.write_text(json.dumps(order_json, indent=2))

            is_yes = inquirer.confirm("You quit")
            if is_yes:
                break

    if len(argv) > 1:
        break
