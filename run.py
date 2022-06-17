from app import *
from multiprocessing import Process


if __name__ == "__main__":
    init_db()

    process = Process(
        target=insert_data_on_table)
    process.start()
