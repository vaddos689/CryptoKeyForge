def write_list_to_file(lst, filename):
    with open(filename, 'w') as f:
        for item in lst:
            f.write(str(item) + '\n')
    print(f"Данные успешно записаны в файл {filename}")
