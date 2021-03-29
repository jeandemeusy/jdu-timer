from display import color, warning, error
import time


class Singleton(type):
    """
    Singleton class to inherit from to create a new singleton.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(
                Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Timer(metaclass=Singleton):
    """
    Class made to measure execution time easily, and get a summary of all measurements.
    """

    def __init__(self):
        """
        Initialisation class for timer.
        """

        self.funcs = []         # list of block functions
        self.times = []         # list of block times in ms
        self.titles = []        # list of block titles
        self.__subfuncs = []    # current block functions
        self.__subtimes = []    # current block times in ms
        self.__blocktimes = []  # list of total block time in ms

    def add(self, func, *args):
        """
        Get function execution time, and adds it to an array for later use.
        For display, call pack() then print_block() or final_print().
        """

        start_time = time.time()
        ret = func(*args)
        end_time = time.time()

        self.__subtimes.append((end_time - start_time)*1000)
        self.__subfuncs.append(func.__name__)

        return ret

    def pack(self, title):
        """
        Takes current timed functions results and stores it as a block with a given title. For display, call print_block() or final_print().
        """

        self.titles.append(title)
        self.funcs.append(self.__subfuncs)
        self.times.append(self.__subtimes)
        self.__blocktimes.append(sum(self.__subtimes))
        self.__subfuncs = []
        self.__subtimes = []

    def show_block(self, id=-1):
        """
        Prints block with given id. id can be an integer or the name of the block.
        """

        if isinstance(id, str):
            try:
                id = self.titles.index(id)
            except:
                error("timer block not found.")

        if isinstance(id, int):
            try:
                l_func = len(max(self.funcs[id], key=len))
                for func, time in zip(self.funcs[id], self.times[id]):
                    self.__print(" ", func, time, 0, l_func)
            except:
                error("id out of range.")

    def show(self):
        """
        Prints all blocks, with title, and inner functions execution time.
        """

        l_func = max([len(max(f, key=len)) for f in self.funcs])
        l_title = len(max(self.titles, key=len))

        for i, (b_func, b_time, title) in enumerate(self.__summary()):
            self.__print(title, "", 0, l_title, 0, color.BOLD)

            for func, time in zip(b_func, b_time):
                self.__print(" ", func, time, l_title, l_func)

            self.__print("", " ", self.__blocktimes[i],
                         l_title, l_func, tag=color.GREEN)

        self.__print("", '-'*l_func, 0, l_title, l_func)
        self.__print("", "TOTAL (packed)", sum(self.__blocktimes),
                     l_title, l_func, color.BOLD + color.GREEN)

        if len(self.__subtimes) != 0:
            print('\n')
            warning(
                f"some timed functions are not packed yet.\nCall {self.__name()}().pack() to stack them.")
            self.__print("UNPACKED", "", 0, l_title, 0, color.BOLD)

            for func, time in zip(self.__subfuncs, self.__subtimes):
                self.__print(" ", func, time, l_title, l_func)

    def __print(_, str1, str2, time, len1, len2, tag=color.END):
        """
        Inner-class print format method.
        """

        string = f"{str2:<{len2}}"

        if len1 != 0:
            string = f"{str1:<{len1+1}}" + string

        if time != 0:
            string = string + " "*3 + f"{time:7.2f}ms"

        print(tag + string + color.END)

    def __summary(self):
        """
        Inner-class to zip all block related attributes.
        """

        return zip(self.funcs, self.times, self.titles)

    def __name(self):
        """
        Proxy for class name.
        """

        return self.__class__.__name__

    def __str__(self):
        """
        Short instance description.
        """

        strings = []
        strings.append(
            f"{self.__name()} class with {len(self.titles)} blocks packed:")

        for b_func, _, title in self.__summary():
            strings.append(f"\t- {title} ({', '.join(b_func)})")

        return '\n'.join(strings)
