from typing import Optional


class Matrix:
    """
    Код нашего коллеги аналитика
    Очень медленный и тяжелый для восприятия. Ваша задача сделать его быстрее и проще для понимания.
    """

    def __init__(self):
        self.data = []
        self.size = 1

    def matrix_scale(self, scale_up: bool):
        """
        Функция отвечает за создание увеличенной или уменьшенной матрицы.
        Режим работы зависит от параметра scale_up. На выходе получаем расширенную матрицу.
        :param matrix: исходная матрица
        :param scale_up: если True, то увеличиваем матрицу, иначе уменьшаем
        :return: измененная матрица
        """
        if scale_up:
            self.size += 1
        else:
            self.size -= 1

    def add_item(self, element: Optional = None):
        """
        Добавляем новый элемент в матрицу.
        Если элемент не умещается в (size - 1) ** 2, то расширить матрицу.
        """
        if element is None:
            raise ValueError

        if len(self.data) >= (self.size - 1) ** 2:
            self.matrix_scale(scale_up=True)

        self.data.append(element)

    def pop(self):
        """
        Удалить последний значащий элемент из массива.
        Если значащих элементов меньше (size - 1) * (size - 2) уменьшить матрицу.
        """
        if self.size == 1:
            raise IndexError()

        value = self.data.pop()

        if len(self.data) <= (self.size - 1) * (self.size - 2):
            self.matrix_scale(scale_up=False)

        return value

    def __str__(self):
        """
        Метод должен выводить матрицу в виде:
        1 2 3\nNone None None\nNone None None
        То есть между элементами строки должны быть пробелы, а строки отделены \n
        """
        result = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                index = self.size * i + j
                if index < len(self.data):
                    row.append(str(self.data[index]))
                else:
                    row.append(str(None))

            result.append(' '.join(row))

        return '\n'.join(result)


if __name__ == '__main__':
    m = Matrix()
    m.add_item(1)
    print(m)