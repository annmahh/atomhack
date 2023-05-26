import os
from pathlib import Path
from xml.dom.minidom import parse
import shutil


def copy_files(from_path: str, to_path: str, required_files: list = None) -> None:
    if not os.path.isdir(to_path):
        Path(to_path).mkdir(parents=True)
    # если xml файл есть:
    xml_from_path = from_path.replace('.files', '.xml')
    xml_to_path = to_path.replace('.files', '.xml')
    shutil.copy(xml_from_path, xml_to_path)

    for f in os.scandir(from_path):
        # TODO: сверка файлов с указанными в xml
        # если есть в хмл и есть в папке, то копируем
        # если есть в хмл и нет в папке, то в лог ошибка
        # если есть в папке и нет в хмл, то ошибка
        file_to_path = os.path.join(to_path, f)
        shutil.copy(from_path, file_to_path)


def copy_folder(folder_to_check: str, save_path: str, package_number: str, add_folders: str, path: str,
                required_files: list = None) -> None:
    if os.path.isdir(folder_to_check):
        new_path = os.path.join(save_path, package_number, add_folders) + os.path.join(
            folder_to_check.replace(path, ''))
        copy_files(folder_to_check, new_path, required_files=required_files)
    else:
        pass
        # TODO: запись в лог, что папка отсутствует


def get_xml_path(path: object, obj_type: object) -> str:
    if os.path.isfile(path):
        if obj_type == list:
            if path.endswith('.xml'):
                return path
            else:
                return None
        else:
            if path.name.endswith('.xml'):
                return path.path
            else:
                return None


def collect_packages(path: str, save_path: str) -> str:
    orders_packages = {}
    check_again = []
    content1 = os.scandir(path)

    for c1 in content1:
        if c1.is_dir():
            folder_path = c1.path
            content2 = os.scandir(folder_path)
            content2_type = type(content2)

            for c2 in content2:
                xml_path = get_xml_path(c2, content2_type)
                if xml_path is not None:
                    folder_to_check = xml_path.replace('.xml', '.files')
                    xml = parse(xml_path)
                    objects = xml.getElementsByTagName('object')

                    for o in objects:
                        required_files = []
                        files = o.getElementsByTagName('file')

                        for f in files:
                            f_data = dict(f.attributes.items())
                            f_name = f_data['name']
                            required_files.append(f_name)

                        orders = []
                        rows = o.getElementsByTagName('row')

                        for r in rows:
                            r_order = dict(r.attributes.items())
                            order_number = r_order['order']
                            orders.append(order_number)

                        attributes = o.getElementsByTagName('attribute')
                        for a in attributes:
                            curr_attrs = dict(a.attributes.items())

                            if curr_attrs['name'] == 'A_Package_Number':  # Это комплекты РД
                                package_number = curr_attrs['value']
                                copy_folder(folder_to_check, save_path, package_number, 'Docs', path)
                                break

                            elif curr_attrs['name'] == 'A_Name':
                                doc_name = curr_attrs['value'].lower()
                                if 'чек' in doc_name and 'лист' in doc_name:  # Это чек-листы
                                    package_number = doc_name.split('_')[-1]
                                    copy_folder(folder_to_check, save_path, package_number, 'AccDocs/CheckList', path)
                                    for order in orders:
                                        orders_packages[order] = package_number
                                    break

                            if curr_attrs['name'] == 'A_Name':
                                doc_name = curr_attrs['value'].lower()
                                if 'сопроводительное' in doc_name and 'письмо' in doc_name:  # Это IKL
                                    packages_numbers = list(
                                        set([orders_packages[ordr] for ordr in orders if ordr in orders_packages]))
                                    if len(packages_numbers) == 0:
                                        check_again.append(xml_path)
                                    elif len(packages_numbers) == 1:
                                        package_number = packages_numbers[0]
                                        copy_folder(folder_to_check, save_path, package_number, 'AccDocs/IKL', path)
                                    else:
                                        pass  # TODO: записать ошибку в файл логов
                                    break

                            if curr_attrs['name'] == 'A_Name':
                                doc_name = curr_attrs['value'].lower()
                                if 'пояснительная' in doc_name and 'записка' in doc_name:  # Это Notes
                                    package_number = doc_name.split('_')[-1]
                                    copy_folder(folder_to_check, save_path, package_number, 'AccDocs/Notes', path)
                                    break

                            if curr_attrs['name'] == 'A_Name':
                                doc_name = curr_attrs['value'].lower()
                                if 'пдтк' in doc_name:  # Это PDTK
                                    packages_numbers = list(
                                        set([orders_packages[ordr] for ordr in orders if ordr in orders_packages]))
                                    if len(packages_numbers) == 0:
                                        check_again.append(xml_path)
                                    elif len(packages_numbers) == 1:
                                        package_number = packages_numbers[0]
                                        copy_folder(folder_to_check, save_path, package_number, 'AccDocs/PDTK', path)
                                    else:
                                        pass  # TODO: записать ошибку в файл логов
                                    break

            # TODO: нет xml файлов в content2, проверить на ведомость РД
            # TODO: сформировать в пакетах рд файл с paths

    content2_type = type(check_again)
    for c2 in check_again:
        xml_path = get_xml_path(c2, content2_type)
        if xml_path is not None:
            folder_to_check = xml_path.replace('.xml', '.files')
            xml = parse(xml_path)
            objects = xml.getElementsByTagName('object')

            for o in objects:
                required_files = []
                files = o.getElementsByTagName('file')

                for f in files:
                    f_data = dict(f.attributes.items())
                    f_name = f_data['name']
                    required_files.append(f_name)

                orders = []
                rows = o.getElementsByTagName('row')

                for r in rows:
                    r_order = dict(r.attributes.items())
                    order_number = r_order['order']
                    orders.append(order_number)

                attributes = o.getElementsByTagName('attribute')

                for a in attributes:
                    curr_attrs = dict(a.attributes.items())

                    if curr_attrs['name'] == 'A_Package_Number':  # Это комплекты РД
                        package_number = curr_attrs['value']
                        copy_folder(folder_to_check, save_path, package_number, 'Docs', path)
                        break

                    elif curr_attrs['name'] == 'A_Name':
                        doc_name = curr_attrs['value'].lower()
                        if 'чек' in doc_name and 'лист' in doc_name:  # Это чек-листы
                            package_number = doc_name.split('_')[-1]
                            copy_folder(folder_to_check, save_path, package_number, 'AccDocs/CheckList', path)
                            for order in orders:
                                orders_packages[order] = package_number
                            break

                    if curr_attrs['name'] == 'A_Name':
                        doc_name = curr_attrs['value'].lower()
                        if 'сопроводительное' in doc_name and 'письмо' in doc_name:  # Это IKL
                            packages_numbers = list(
                                set([orders_packages[ordr] for ordr in orders if ordr in orders_packages]))
                            if len(packages_numbers) == 0:
                                # check_again.append(xml_path)
                                pass
                            elif len(packages_numbers) == 1:
                                package_number = packages_numbers[0]
                                copy_folder(folder_to_check, save_path, package_number, 'AccDocs/IKL', path)
                            else:
                                pass  # TODO: записать ошибку в файл логов
                            break

                    if curr_attrs['name'] == 'A_Name':
                        doc_name = curr_attrs['value'].lower()
                        if 'пояснительная' in doc_name and 'записка' in doc_name:  # Это Notes
                            package_number = doc_name.split('_')[-1]
                            copy_folder(folder_to_check, save_path, package_number, 'AccDocs/Notes', path)
                            break

                    if curr_attrs['name'] == 'A_Name':
                        doc_name = curr_attrs['value'].lower()
                        if 'пдтк' in doc_name:  # Это PDTK
                            packages_numbers = list(
                                set([orders_packages[ordr] for ordr in orders if ordr in orders_packages]))
                            if len(packages_numbers) == 0:
                                pass
                            elif len(packages_numbers) == 1:
                                package_number = packages_numbers[0]
                                copy_folder(folder_to_check, save_path, package_number, 'AccDocs/PDTK', path)
                            else:
                                pass  # TODO: записать ошибку в файл логов
                            break


if __name__ == '__main__':
    path = 'example'
    save_path = 'example_collected'
    collect_packages(path, save_path)