#!/usr/bin/python3
"""
The console module provides the `HBNBCommand` class for AirBnb
command intepreter.
"""

import cmd
import re
import shlex
from models import storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class HBNBCommand(cmd.Cmd):
    """HBNBCommand class defines `AirBnb` line-oriented interpreter"""
    intro = ""
    prompt: str = "(hbnb) "

    c_names = {
        'BaseModel': BaseModel,
        'User': User,
        'State': State,
        'City': City,
        'Amenity': Amenity,
        'Place': Place,
        'Review': Review
    }

    def do_quit(self, arg):
        """ Quit the console session """
        return True

    def do_EOF(self, arg):
        """ Quits the console session """
        print()
        return True

    def emptyline(self):
        """ Respond to empty line command """
        pass

    def precmd(self, line: str) -> str:
        """
        Hook method executed just before the command
        line is interpreted, but after the input prompt is
        generated and issued.
        """
        matches = re.findall(r"^(\w+)\.(\w+)\((.*)\)$", line)
        if matches:  # array is not empty
            [cls, method, params] = matches[0]
            args = params = str(params).strip()
            if params:
                args = params.replace(", ", " ")
            return "{} {} {}".format(method, cls, args)

        return super().precmd(line)

    def do_create(self, arg):
        """ Creates a new instance of `BaseModel` """
        if len(arg) == 0:
            print("** class name missing **")
            return False

        if arg not in HBNBCommand.c_names.keys():
            print("** class doesn't exist **")
            return False

        m = HBNBCommand.c_names[arg]()
        m.save()
        print(m.id)

    def do_show(self, arg):
        """
        Prints the string representation of an instance based
        on the className
        """
        arr = self.__get_class_args(arg)
        if not arr:
            return False

        if len(arr) < 2:
            print("** instance id missing **")
            return False

        cls, id = arr[0], arr[1]
        key = "{}.{}".format(cls, id)

        if key not in storage.all():
            print("** no instance found **")
        else:
            obj = storage.all()[key]
            print(obj)

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id """
        arr = self.__get_class_args(arg)
        if not arr:
            return False

        if len(arr) < 2:
            print("** instance id missing **")
            return False

        cls, id = arr[0], arr[1]
        key = "{}.{}".format(cls, id)

        if key not in storage.all():
            print("** no instance found **")
        else:
            # using name mangling `storage._FileStorage__objects`
            # del storage._FileStorage__objects[key]
            del storage.all()[key]
            storage.save()

    def do_all(self, arg):
        """ Prints all string representation of all instances
        based or not on the class name
        """
        cls = None
        if arg:
            arr = self.__get_class_args(arg)
            if not arr:     # class name is not valid?
                return False
            cls = arr[0]

        if not cls:     # get all
            print([str(v) for v in storage.all().values()])
        else:
            print([
                str(v)
                for k, v in storage.all().items()
                if str(k).split(".")[0] == cls
            ])

    def do_update(self, arg):
        """ Updates an instance based on the class name and id """
        arr = self.__get_class_args(arg)
        if not arr:
            return False

        if len(arr) < 2:
            print("** instance id missing **")
            return False

        cls, id = arr[0], arr[1]
        key = "{}.{}".format(cls, id)

        if key not in storage.all():
            print("** no instance found **")
            return False

        obj = storage.all()[key]
        if len(arr) < 3:
            print("** attribute name missing **")
            return False

        if len(arr) < 4:
            print("** value missing **")
            return False

        attr, val = arr[2], arr[3]
        setattr(obj, attr, val)
        obj.save()

    def do_count(self, arg):
        """ Get count of persisted instances """
        cls = None
        if arg:
            arr = self.__get_class_args(arg)
            if not arr:     # class name is not valid?
                return False
            cls = arr[0]

        if not cls:     # get all
            print(len([str(v) for v in storage.all().values()]))
        else:
            print(len([
                str(v)
                for k, v in storage.all().items()
                if str(k).split(".")[0] == cls
            ]))

    def __get_class_args(self, arg: str):
        """
        Gets the arguments in a command
        Format: <class_name> (...params)
        """
        if not arg:
            print("** class name missing **")
            return None

        s_args = shlex.split(arg)

        if s_args[0] not in HBNBCommand.c_names.keys():
            print("** class doesn't exist **")
            return None

        return s_args


if __name__ == "__main__":
    HBNBCommand().cmdloop()
