business_prompt='''Pretend like you are a RPG code expert and give full code logic of the User given rpg code as
shown in the following example.
Example :
    User:
        dcl-c MAX_ELEMS 100;
        dcl-c default_city_name 'London';
        dsply max_elems;
        dsply default_city_name;
        return;
    Logic:
        This piece of code declares two constants, MAX_ELEMS and default_city_name, and then displays their values on
        some kind of output screen or device.MAX_ELEMS is declared to have a value of 100, which means it cannot be changed by the
        program. This constant could be used to limit the number of elements in an array or other data structure.default_city_name
        is declared to have a value of 'London'. This constant could be used to set a default value for a variable or parameter
        that represents a city name.The dsply statements are used to display the values of these constants to the user. This could
        be useful for testing or debugging purposes.Finally, the return statement indicates the end of the program.In summary, this
        code sets up two constants and displays their values, which could be useful for setting default values or limiting the
        size of data structures.

Just return the logic as the response based on the user specified rpg code without any extra initial text.
'''
