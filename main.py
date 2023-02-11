from manager import Manager


def get_query(filename):
    file = open("tests/" + filename + ".sql", "r")
    text = file.read()
    return text


def get_result(filename):
    file = open("results/" + filename + ".sql", "r")
    text = file.read()
    return text


def run_tests(tests):
    m = Manager("database")
    for test in tests:
        my_result = m.execute(get_query(test))
        print(my_result)
        # result = get_result(test)
        # if my_result != result:
        #     print(f"Wrong {test}!")


if __name__ == '__main__':
    sample_database = "sample_database"
    test_people = "people"
    test_colors ="colors"
    test_likes = "likes"
    test_join = "test_join"
    test_where = "test_where"
    test_group_by = "test_group_by"
    test_having = "test_having"
    test_order_by = "test_order_by"
    # test1 = "test1"
    # test2 = "test2"
    # test3 = "test3"
    # test4 = "test4"
    # test5 = "test5"

    tests = [
        test_people,
        test_colors,
        test_likes,
        test_join,
        test_where,
        test_group_by,
        test_having,
        test_order_by,
        # test1,
        # test2,
        # test3,
        # test4,
        # test5
    ]

    m = Manager("database")
    # m.execute(get_query(sample_database))

    my_result = m.execute(get_query(test_order_by))
    print(my_result)


    # run_tests(tests)




