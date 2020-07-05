from typing import Optional, List, Tuple


class Matrix:
    """
    Код нашего коллеги аналитика
    Очень медленный и тяжелый для восприятия. Ваша задача сделать его быстрее и проще для понимания.
    """

    def __init__(self):
        self.matrix = [[None]]

    @staticmethod
    def get_indices_from_order_number(order_number: int, size: int) -> Tuple[int, int]:
        return (order_number // size, order_number % size)

    @staticmethod
    def get_order_number_from_indices(i: int, j: int, size: int) -> int:
        return i * size + j

    def _matrix_scale_up(self, matrix: List[List[Optional[object]]]) -> List[List[Optional[object]]]:
        old_size = len(matrix)
        new_size = old_size + 1

        new_matrix = [[None for _ in range(new_size)] for _ in range(new_size)]

        for old_i in range(old_size):
            for old_j in range(old_size):
                old_order_n = self.get_order_number_from_indices(old_i, old_j, old_size)
                new_i, new_j = self.get_indices_from_order_number(old_order_n, new_size)
                new_matrix[new_i][new_j] = matrix[old_i][old_j]

        return new_matrix

    def _matrix_scale_down(self, matrix: List[List[Optional[object]]])-> List[List[Optional[object]]]:
        old_size = len(matrix)
        new_size = old_size - 1

        new_matrix = [[None for _ in range(new_size)] for _ in range(new_size)]

        for new_i in range(new_size):
            for new_j in range(new_size):
                new_order_n = self.get_order_number_from_indices(new_i, new_j, old_size)
                old_i, old_j = self.get_indices_from_order_number(new_order_n, new_size)
                new_matrix[new_i][new_j] = matrix[old_i][old_j]

        return new_matrix

    def matrix_scale(self, matrix: List[List[Optional[object]]], scale_up: bool) -> List[List[Optional[object]]]:
        """
        Функция отвечает за создание увеличенной или уменьшенной матрицы.
        Режим работы зависит от параметра scale_up. На выходе получаем расширенную матрицу.
        :param matrix: исходная матрица
        :param scale_up: если True, то увеличиваем матрицу, иначе уменьшаем
        :return: измененная матрица
        """
        if scale_up:
            return self._matrix_scale_up(matrix)
        else:
            return self._matrix_scale_down(matrix)

    def find_first_none_position(self, matrix) -> (int, int):
        """
        Находим позицию в матрице первого None элемента. По сути он обозначает конец данных матрицы.
        """
        for row in range(len(matrix)):
            for column in range(len(matrix)):
                if matrix[row][column] is None:
                    return row, column

    def find_last_not_none_position(self, matrix):
        """
        Находим позицию последнего не None элемента матрицы.
        """
        for row in range(len(matrix) - 1, -1, -1):
            for column in range(len(matrix) - 1, -1, -1):
                if matrix[row][column] is not None:
                    return row, column

    def add_item(self, element: Optional = None):
        """
        Добавляем новый элемент в матрицу.
        Если элемент не умещается в (size - 1) ** 2, то расширить матрицу.
        """
        if element is None:
            raise ValueError

        size = len(self.matrix)
        last_row, last_column = self.find_first_none_position(self.matrix)

        if last_row * size + last_column >= (size - 1) ** 2:
            self.matrix = self.matrix_scale(self.matrix, scale_up=True)
            last_row, last_column = self.find_first_none_position(self.matrix)

        self.matrix[last_row][last_column] = element

    def pop(self):
        """
        Удалить последний значащий элемент из массива.
        Если значащих элементов меньше (size - 1) * (size - 2) уменьшить матрицу.
        """
        size = len(self.matrix)
        if size == 1:
            raise IndexError()

        last_row, last_column = self.find_last_not_none_position(self.matrix)
        value = self.matrix[last_row][last_column]
        self.matrix[last_row][last_column] = None

        if last_row * size + last_column <= (size - 1) * (size - 2):
            self.matrix = self.matrix_scale(self.matrix, scale_up=False)

        return value

    def __str__(self):
        """
        Метод должен выводить матрицу в виде:
        1 2 3\nNone None None\nNone None None
        То есть между элементами строки должны быть пробелы, а строки отделены \n
        """
        result = []
        for row in range(len(self.matrix)):
            result.append(' '.join(str(x) for x in self.matrix[row]))

        return '\n'.join(result)


if __name__ == '__main__':
    pass
