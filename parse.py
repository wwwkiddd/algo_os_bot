def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"Файл '{file_path}' не найден."
    except Exception as e:
        return f"Произошла ошибка при чтении файла: {e}"
