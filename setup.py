import cx_Freeze

executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="Ice Block Puzzle Game",
    options={"build_exe": {"packages":["pygame"],
                           "include_files":["fonts/8-bitlimitobrk.ttf"]}},
    executables = executables

    )