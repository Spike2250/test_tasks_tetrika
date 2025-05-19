from typing import Dict, Tuple


def strict(func):
    def wrapper(*args, **kwargs):

        annotations = func.__annotations__

        def _args_to_kwargs(func_args: Tuple, func_annotations: Dict) -> Dict:
            args_names = list(func_annotations.keys())
            return {args_names[i]: func_arg for i, func_arg in enumerate(func_args)}

        # переводим кортеж аргументов в словарь
        kw_args = _args_to_kwargs(args, annotations)

        # Проверка соответствия типов данных
        for arg in kw_args:
            # сообщение ошибки
            error_msg = f"Тип переданных данных для аргумента '{arg}' "\
                        f"функции '{func.__name__}' не соответствует "\
                        f"аннотированному!!!\n"\
                        f"\t\tОжидаемый тип данных: {annotations[arg]}\n"\
                        f"\t\tПереданный тип данных: {type(kw_args[arg])}"

            # для целых чисел отдельно (ввиду того, что в python bool является подклассом int и
            # при аннотированом типе int при передаче True/False они считаются валидными)
            if isinstance(annotations[arg], type(int)):
                if isinstance(kw_args[arg], bool):
                    raise TypeError(error_msg)
                elif not isinstance(kw_args[arg], annotations[arg]):
                    raise TypeError(error_msg)
            # для всех остальных
            elif not isinstance(kw_args[arg], annotations[arg]):
                raise TypeError(error_msg)

        # результат функции
        result = func(*args, **kwargs)
        return result
    return wrapper
