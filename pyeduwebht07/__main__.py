import sys
import logging
from my_select import *
import pretty_tables


def show_query_results(query_func):
    func_name = f' {query_func.__doc__} '
    header = f'{func_name:#^80}'
    print(header)

    if data := query_func():
        if not (data[0] and data[1]):
            print('We got an empty set! Check the parameters of the query!')
        else:
            pretty = pretty_tables.create(headers=data[0], rows=[list(d) for d in data[1]])
            print(pretty)

    print(f'{"#" * len(header)}')


def main():
    print(f'01. Executing SQLAlchemy queries from "my_select.py" file...')

    for select_func in (funcs := (select_1, select_2, select_3, select_4, select_5,
                                  select_6, select_7, select_8, select_9, select_10,
                                  select_11, select_12)):
        show_query_results(select_func)

        if select_func != list(funcs)[-1]:
            try:
                answer = input("Next task? (Y/n): ").strip()
                print()
                if answer and answer.lower() != 'y':
                    sys.exit()
            except (KeyboardInterrupt, EOFError):
                print()
                sys.exit()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    sys.exit(main())
