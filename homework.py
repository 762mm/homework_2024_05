from datetime import datetime


def read_file(file_name):
    "Чтение и обработка файла из директории 'source'."

    with open('source\\' + file_name, 'r', encoding='ANSI') as f:
        data = {}
        for i, line in enumerate(f):
            row = [x[1:-1] for x in line[:-1].split(';')]

            if i:
                row[-1] = datetime.strptime(row[-1], '%d.%m.%Y')
                row[-2] = datetime.strptime(row[-2], '%d.%m.%Y')

            data[i] = row
    print(f'Файл с данными {file_name} загружен.')
    return data


def write_file(file_name, data):
    "Запись результатов в файл."

    output_file = open('result\\' + file_name, 'a', encoding='ANSI')
    for line in data:
        output_file.write(line + '\r')
    output_file.close()
    print(
        f'Файл с результатами {file_name} сформирован в директории "result".'
    )


def all_versions(data_register, data_reference):
    "Обработка и объединение данных."

    result_data = ['"Наименование";"Форма";"Код города";"Название города"']

    for i in range(len(data_register))[1:]:
        join_check = 0
        row = [data_register[i][2], data_register[i][1]]
        for k in range(len(data_reference))[1:]:
            if (
                    data_register[i][3] == data_reference[k][0]
                    and data_register[i][4] < data_reference[k][4]
                    and data_register[i][5] > data_reference[k][3]
            ):
                join_check = 1
                result_data.append(
                    '"'+'";"'.join(row.copy() + [
                        data_reference[k][1], data_reference[k][2]
                    ])+'"'
                )
        if not join_check:
            result_data.append('"'+'";"'.join(row.copy() + ['', ''])+'"')

    return result_data


if __name__ == '__main__':

    data_register = read_file('register.csv')

    data_reference = read_file('reference.csv')

    result_data = all_versions(data_register, data_reference)

    write_file('result.csv', result_data)
